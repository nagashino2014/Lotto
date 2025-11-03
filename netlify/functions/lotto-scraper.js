// 네이버 로또 당첨 번호 스크래핑 (Cheerio 없이)
exports.handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json',
  };

  // CORS preflight 처리
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const round = event.queryStringParameters?.round;

  if (!round) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({ error: 'Round parameter is required' }),
    };
  }

  try {
    // 1차 시도: 동행복권 API
    try {
      const apiUrl = `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`;
      const response = await fetch(apiUrl);
      
      if (response.ok) {
        const data = await response.json();
        
        // 미추첨 회차 확인
        if (data.returnValue === 'fail') {
          return {
            statusCode: 404,
            headers,
            body: JSON.stringify({ error: 'Draw not completed yet' }),
          };
        }
        
        // 정상 응답
        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            round: data.drwNo,
            date: data.drwNoDate,
            numbers: [
              data.drwtNo1,
              data.drwtNo2,
              data.drwtNo3,
              data.drwtNo4,
              data.drwtNo5,
              data.drwtNo6,
            ].sort((a, b) => a - b),
            bonus: data.bnusNo,
            prize: {
              1: { count: data.firstPrzwnerCo || 0, amount: data.firstWinamnt || 0 },
              2: { count: data.secondPrzwnerCo || 0, amount: data.secondWinamnt || 0 },
              3: { count: data.thirdPrzwnerCo || 0, amount: data.thirdWinamnt || 0 },
              4: { count: data.fourthPrzwnerCo || 0, amount: 50000 },
              5: { count: data.fifthPrzwnerCo || 0, amount: 5000 },
            },
          }),
        };
      }
    } catch (apiError) {
      console.log('동행복권 API 실패, 네이버 스크래핑 시도:', apiError.message);
    }

    // 2차 시도: 네이버 검색 결과 스크래핑
    const naverUrl = `https://search.naver.com/search.naver?query=로또+${round}회차`;
    const naverResponse = await fetch(naverUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });

    if (!naverResponse.ok) {
      throw new Error('네이버 검색 실패');
    }

    const html = await naverResponse.text();
    
    // HTML에서 로또 번호 추출 (정규식 사용)
    const result = {
      round: parseInt(round),
      date: '',
      numbers: [],
      bonus: 0,
      prize: {
        1: { count: 0, amount: 0 },
        2: { count: 0, amount: 0 },
        3: { count: 0, amount: 0 },
        4: { count: 0, amount: 50000 },
        5: { count: 0, amount: 5000 },
      }
    };

    // 당첨 번호 추출 시도 (네이버 로또 위젯의 class 이름 기반)
    // 예: <span class="ball_645 lrg ball1">1</span>
    const ballRegex = /ball_645[^>]*>(\d+)</g;
    const balls = [];
    let match;
    while ((match = ballRegex.exec(html)) !== null && balls.length < 7) {
      balls.push(parseInt(match[1]));
    }

    if (balls.length === 7) {
      result.numbers = balls.slice(0, 6).sort((a, b) => a - b);
      result.bonus = balls[6];
    }

    // 추첨일 추출
    const dateRegex = /(\d{4}\.\d{2}\.\d{2})/;
    const dateMatch = html.match(dateRegex);
    if (dateMatch) {
      result.date = dateMatch[1];
    }

    // 당첨금 추출 시도
    const prizeRegex = /(\d+(?:,\d+)*)\s*원/g;
    const prizes = [];
    let prizeMatch;
    while ((prizeMatch = prizeRegex.exec(html)) !== null && prizes.length < 5) {
      const amount = parseInt(prizeMatch[1].replace(/,/g, ''));
      if (amount > 1000) { // 1000원 이상만 (광고 등 필터링)
        prizes.push(amount);
      }
    }

    // 1~3등 당첨금 설정
    if (prizes.length >= 3) {
      result.prize[1].amount = prizes[0];
      result.prize[2].amount = prizes[1];
      result.prize[3].amount = prizes[2];
    }

    // 번호가 추출되지 않았다면 오류
    if (result.numbers.length === 0) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ 
          error: 'Could not extract lottery numbers',
          hint: '회차 정보를 찾을 수 없습니다. 올바른 회차를 입력했는지 확인해주세요.'
        }),
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(result),
    };

  } catch (error) {
    console.error('스크래핑 오류:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Failed to fetch lottery data',
        details: error.message
      }),
    };
  }
};

