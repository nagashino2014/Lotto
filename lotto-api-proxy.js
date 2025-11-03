// netlify/functions/lotto-api.js
// Netlify Functions를 사용한 로또 당첨번호 API 프록시

const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // CORS 헤더 설정
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // OPTIONS 요청 처리 (CORS preflight)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // 회차 번호 파라미터 가져오기
  const round = event.queryStringParameters?.round;
  
  if (!round) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: '회차 번호를 입력해주세요.' })
    };
  }

  try {
    // 동행복권 공식 API 호출
    const response = await fetch(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
    );
    
    if (!response.ok) {
      throw new Error('동행복권 API 호출 실패');
    }

    const data = await response.json();
    
    // 데이터가 유효한지 확인
    if (data.returnValue !== 'success') {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ 
          error: `${round}회차 정보를 찾을 수 없습니다.`,
          message: '아직 추첨되지 않았거나 잘못된 회차 번호입니다.'
        })
      };
    }

    // 응답 데이터 정리 및 반환
    const result = {
      round: data.drwNo,
      date: data.drwNoDate,
      numbers: [
        data.drwtNo1,
        data.drwtNo2,
        data.drwtNo3,
        data.drwtNo4,
        data.drwtNo5,
        data.drwtNo6
      ].sort((a, b) => a - b),
      bonus: data.bnusNo,
      prize: {
        1: {
          count: data.firstPrzwnerCo,
          amount: data.firstWinamnt,
          totalAmount: data.firstAccumamnt
        },
        2: {
          count: data.secondPrzwnerCo || 0,
          amount: data.secondWinamnt || 0,
          totalAmount: data.secondAccumamnt || 0
        },
        3: {
          count: data.thirdPrzwnerCo || 0,
          amount: data.thirdWinamnt || 0,
          totalAmount: data.thirdAccumamnt || 0
        },
        4: {
          count: data.fourthPrzwnerCo || 0,
          amount: 50000,
          totalAmount: (data.fourthPrzwnerCo || 0) * 50000
        },
        5: {
          count: data.fifthPrzwnerCo || 0,
          amount: 5000,
          totalAmount: (data.fifthPrzwnerCo || 0) * 5000
        }
      },
      totalSellAmount: data.totSellamnt,
      returnRate: data.returnRate,
      drwNumber: {
        1: data.drwtNo1,
        2: data.drwtNo2,
        3: data.drwtNo3,
        4: data.drwtNo4,
        5: data.drwtNo5,
        6: data.drwtNo6,
        bonus: data.bnusNo
      }
    };
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(result)
    };
    
  } catch (error) {
    console.error('Error fetching lottery data:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: '서버 오류가 발생했습니다.',
        message: error.message
      })
    };
  }
};

// ===================================================================
// 또는 Express.js를 사용한 독립 서버 (server.js)
// ===================================================================

/*
const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();
const PORT = process.env.PORT || 3000;

// CORS 설정
app.use(cors());
app.use(express.json());

// 헬스체크 엔드포인트
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// 최신 회차 조회
app.get('/api/lotto/latest', async (req, res) => {
  try {
    // 최신 회차 계산 (매주 토요일 추첨)
    const today = new Date();
    const firstLotto = new Date('2002-12-07');
    const daysDiff = Math.floor((today - firstLotto) / (1000 * 60 * 60 * 24));
    const weeksPassed = Math.floor(daysDiff / 7);
    const latestRound = weeksPassed + 1;
    
    // 최신 회차 정보 조회
    const response = await axios.get(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${latestRound}`
    );
    
    if (response.data.returnValue !== 'success') {
      // 아직 추첨 전이면 이전 회차 조회
      const prevResponse = await axios.get(
        `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${latestRound - 1}`
      );
      res.json(formatLottoData(prevResponse.data));
    } else {
      res.json(formatLottoData(response.data));
    }
  } catch (error) {
    res.status(500).json({ error: '최신 회차 조회 실패' });
  }
});

// 특정 회차 조회
app.get('/api/lotto/:round', async (req, res) => {
  const round = req.params.round;
  
  try {
    const response = await axios.get(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
    );
    
    if (response.data.returnValue !== 'success') {
      return res.status(404).json({ 
        error: `${round}회차 정보를 찾을 수 없습니다.` 
      });
    }
    
    res.json(formatLottoData(response.data));
  } catch (error) {
    res.status(500).json({ error: '당첨 번호 조회 실패' });
  }
});

// 여러 회차 조회 (배치)
app.post('/api/lotto/batch', async (req, res) => {
  const { rounds } = req.body;
  
  if (!rounds || !Array.isArray(rounds)) {
    return res.status(400).json({ error: '회차 배열이 필요합니다.' });
  }
  
  try {
    const results = await Promise.all(
      rounds.map(async (round) => {
        try {
          const response = await axios.get(
            `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
          );
          
          if (response.data.returnValue === 'success') {
            return formatLottoData(response.data);
          }
          return null;
        } catch (error) {
          return null;
        }
      })
    );
    
    res.json(results.filter(r => r !== null));
  } catch (error) {
    res.status(500).json({ error: '배치 조회 실패' });
  }
});

// 통계 조회
app.get('/api/lotto/stats/:startRound/:endRound', async (req, res) => {
  const { startRound, endRound } = req.params;
  const start = parseInt(startRound);
  const end = parseInt(endRound);
  
  if (end - start > 100) {
    return res.status(400).json({ error: '최대 100회차까지 조회 가능합니다.' });
  }
  
  try {
    const rounds = [];
    for (let i = start; i <= end; i++) {
      rounds.push(i);
    }
    
    const results = await Promise.all(
      rounds.map(async (round) => {
        try {
          const response = await axios.get(
            `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
          );
          
          if (response.data.returnValue === 'success') {
            return formatLottoData(response.data);
          }
          return null;
        } catch (error) {
          return null;
        }
      })
    );
    
    const validResults = results.filter(r => r !== null);
    
    // 통계 계산
    const numberFrequency = {};
    for (let i = 1; i <= 45; i++) {
      numberFrequency[i] = 0;
    }
    
    validResults.forEach(result => {
      result.numbers.forEach(num => {
        numberFrequency[num]++;
      });
    });
    
    const stats = {
      rounds: validResults.length,
      startRound: start,
      endRound: end,
      numberFrequency,
      mostFrequent: Object.entries(numberFrequency)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 6)
        .map(([num, freq]) => ({ number: parseInt(num), frequency: freq })),
      leastFrequent: Object.entries(numberFrequency)
        .sort((a, b) => a[1] - b[1])
        .slice(0, 6)
        .map(([num, freq]) => ({ number: parseInt(num), frequency: freq }))
    };
    
    res.json(stats);
  } catch (error) {
    res.status(500).json({ error: '통계 조회 실패' });
  }
});

// 데이터 포맷팅 함수
function formatLottoData(data) {
  return {
    round: data.drwNo,
    date: data.drwNoDate,
    numbers: [
      data.drwtNo1,
      data.drwtNo2,
      data.drwtNo3,
      data.drwtNo4,
      data.drwtNo5,
      data.drwtNo6
    ].sort((a, b) => a - b),
    bonus: data.bnusNo,
    prize: {
      1: {
        count: data.firstPrzwnerCo,
        amount: data.firstWinamnt,
        totalAmount: data.firstAccumamnt
      },
      2: {
        count: data.secondPrzwnerCo || 0,
        amount: data.secondWinamnt || 0,
        totalAmount: data.secondAccumamnt || 0
      },
      3: {
        count: data.thirdPrzwnerCo || 0,
        amount: data.thirdWinamnt || 0,
        totalAmount: data.thirdAccumamnt || 0
      },
      4: {
        count: data.fourthPrzwnerCo || 0,
        amount: 50000,
        totalAmount: (data.fourthPrzwnerCo || 0) * 50000
      },
      5: {
        count: data.fifthPrzwnerCo || 0,
        amount: 5000,
        totalAmount: (data.fifthPrzwnerCo || 0) * 5000
      }
    },
    totalSellAmount: data.totSellamnt
  };
}

// 서버 시작
app.listen(PORT, () => {
  console.log(`로또 API 프록시 서버가 포트 ${PORT}에서 실행 중입니다.`);
  console.log(`API 문서: http://localhost:${PORT}/api-docs`);
});
*/

// ===================================================================
// package.json (Node.js 서버용)
// ===================================================================
/*
{
  "name": "lotto-api-proxy",
  "version": "1.0.0",
  "description": "로또 당첨번호 조회 API 프록시 서버",
  "main": "server.js",
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "axios": "^1.6.2",
    "node-fetch": "^2.6.9"
  },
  "devDependencies": {
    "nodemon": "^3.0.2"
  }
}
*/