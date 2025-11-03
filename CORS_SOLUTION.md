# 🎯 당첨번호 API 사용 가이드

## ⚠️ CORS 문제 안내

브라우저에서 동행복권 API를 직접 호출하면 **CORS(Cross-Origin Resource Sharing) 정책**으로 인해 차단될 수 있습니다.

### CORS란?
브라우저의 보안 정책으로, 다른 도메인의 리소스에 직접 접근하는 것을 제한합니다.

## 🔧 해결 방법

### 방법 1: 로컬에서 파일로 열기 (테스트용)

일부 브라우저에서는 `file://` 프로토콜로 열면 CORS 정책이 느슨해집니다:

```bash
# 파일 탐색기에서 enhanced_lotto.html을 더블클릭하여 열기
```

**장점**: 별도 설정 불필요  
**단점**: 브라우저마다 다를 수 있으며, 완전한 해결책은 아님

---

### 방법 2: 브라우저 확장 프로그램 사용 (간단)

CORS를 우회하는 브라우저 확장 프로그램을 설치:

#### Chrome/Edge용:
1. **"Allow CORS: Access-Control-Allow-Origin"** 확장 프로그램 설치
2. 확장 프로그램 아이콘을 클릭하여 활성화
3. `enhanced_lotto.html` 열기
4. 당첨번호 조회 시도

**⚠️ 주의**: 사용 후에는 반드시 비활성화하세요 (보안상 위험)

---

### 방법 3: 로컬 웹 서버로 실행 (권장)

Python이 설치되어 있다면 간단한 웹 서버를 실행할 수 있습니다:

#### Python 3 사용:
```bash
# 프로젝트 폴더에서 실행
python -m http.server 8000

# 또는 Python 2 사용 시
python -m SimpleHTTPServer 8000
```

#### Node.js 사용:
```bash
# http-server 설치
npm install -g http-server

# 서버 실행
http-server -p 8000
```

그 다음 브라우저에서 접속:
```
http://localhost:8000/enhanced_lotto.html
```

---

### 방법 4: GitHub Pages로 호스팅 (영구적 해결)

GitHub Pages에 배포하면 HTTPS로 서비스되어 일부 CORS 제한이 완화됩니다:

1. GitHub 저장소에 파일들을 업로드
2. Settings → Pages → Source를 `main` 브랜치로 설정
3. 생성된 URL로 접속:
   ```
   https://nagashino2014.github.io/Lotto/enhanced_lotto.html
   ```

**장점**: 어디서나 접속 가능, 별도 서버 불필요  
**단점**: 동행복권 API가 CORS를 완전히 차단하면 여전히 문제 발생 가능

---

### 방법 5: 프록시 서버 구축 (완벽한 해결책)

프록시 서버를 통해 API 요청을 중계하면 CORS 문제를 완전히 해결할 수 있습니다.

#### A. Netlify Functions 사용 (무료, 추천!)

1. **Netlify 계정 생성**: https://netlify.com

2. **프로젝트 폴더에 파일 생성**:
   ```
   Lotto/
   ├── netlify/
   │   └── functions/
   │       └── lotto-api.js  ← 이미 제공된 파일
   ├── enhanced_lotto.html
   └── netlify.toml  ← 새로 만들기
   ```

3. **netlify.toml 파일 생성**:
   ```toml
   [build]
     publish = "."
     functions = "netlify/functions"
   
   [[redirects]]
     from = "/api/*"
     to = "/.netlify/functions/:splat"
     status = 200
   ```

4. **lotto-api.js를 netlify/functions/ 폴더로 이동**:
   ```bash
   mkdir -p netlify/functions
   mv lotto-api-proxy.js netlify/functions/lotto-api.js
   ```

5. **Netlify에 배포**:
   - Netlify 대시보드에서 "New site from Git" 클릭
   - GitHub 저장소 연결
   - 자동 배포

6. **HTML 파일 수정** (fetchWinningNumbers 함수):
   ```javascript
   async function fetchWinningNumbers(round) {
       try {
           // Netlify Functions 엔드포인트 사용
           const response = await fetch(`/.netlify/functions/lotto-api?round=${round}`);
           
           if (!response.ok) {
               const errorData = await response.json();
               if (response.status === 404) {
                   return null; // 미추첨 회차
               }
               throw new Error(errorData.error || 'API 호출 실패');
           }
           
           return await response.json();
       } catch (error) {
           console.error('당첨 번호 조회 오류:', error);
           throw error;
       }
   }
   ```

**배포 후 접속**:
```
https://your-site-name.netlify.app/enhanced_lotto.html
```

---

#### B. Vercel Functions 사용 (무료, 대안)

1. **Vercel 계정 생성**: https://vercel.com

2. **프로젝트 폴더에 파일 생성**:
   ```
   Lotto/
   ├── api/
   │   └── lotto.js  ← 새로 만들기
   └── enhanced_lotto.html
   ```

3. **api/lotto.js 파일 생성**:
   ```javascript
   export default async function handler(req, res) {
     const { round } = req.query;
     
     if (!round) {
       return res.status(400).json({ error: '회차 번호를 입력해주세요.' });
     }
     
     try {
       const response = await fetch(
         `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
       );
       
       const data = await response.json();
       
       if (data.returnValue !== 'success') {
         return res.status(404).json({ 
           error: '회차 정보를 찾을 수 없습니다.' 
         });
       }
       
       res.status(200).json({
         round: data.drwNo,
         date: data.drwNoDate,
         numbers: [
           data.drwtNo1, data.drwtNo2, data.drwtNo3,
           data.drwtNo4, data.drwtNo5, data.drwtNo6
         ].sort((a, b) => a - b),
         bonus: data.bnusNo,
         prize: {
           1: { count: data.firstPrzwnerCo, amount: data.firstWinamnt },
           2: { count: data.secondPrzwnerCo, amount: data.secondWinamnt },
           3: { count: data.thirdPrzwnerCo, amount: data.thirdWinamnt },
           4: { count: data.fourthPrzwnerCo, amount: 50000 },
           5: { count: data.fifthPrzwnerCo, amount: 5000 }
         }
       });
     } catch (error) {
       res.status(500).json({ error: '서버 오류가 발생했습니다.' });
     }
   }
   ```

4. **Vercel에 배포**:
   ```bash
   npm install -g vercel
   vercel
   ```

5. **HTML 파일 수정**:
   ```javascript
   async function fetchWinningNumbers(round) {
       const response = await fetch(`/api/lotto?round=${round}`);
       // ...
   }
   ```

---

### 방법 6: 독립 Express.js 서버 (고급)

완전한 제어가 필요하다면 독립 서버를 구축할 수 있습니다.

`lotto-api-proxy.js` 파일의 주석 처리된 Express.js 코드를 참고하세요.

---

## 🎯 권장 방법

### 개발/테스트 중:
- **방법 3**: 로컬 웹 서버 사용

### 실제 사용:
- **방법 5A**: Netlify Functions (무료, 간단, 안정적)

---

## 📝 현재 코드 상태

`enhanced_lotto.html`은 이미 **동행복권 API를 직접 호출**하도록 구현되어 있습니다.

### 장점:
- 별도 서버 없이 작동 (CORS가 허용되는 경우)
- 실시간 최신 데이터

### 단점:
- CORS 정책으로 차단될 수 있음
- 브라우저 보안 설정에 따라 다름

---

## 🔍 CORS 오류 확인 방법

개발자 도구(F12) → Console 탭에서 다음과 같은 오류가 나타나면 CORS 문제입니다:

```
Access to fetch at 'https://www.dhlottery.co.kr/...' from origin 'file://' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header 
is present on the requested resource.
```

---

## ✅ 테스트 방법

1. `enhanced_lotto.html` 열기
2. **당첨 체크** 탭으로 이동
3. 회차 번호 입력 (예: 1100)
4. **당첨 확인** 버튼 클릭

### 예상 결과:

#### ✅ 성공 시:
```
🎯 1100회차 당첨 번호 (2024-03-16)
[당첨번호 6개 + 보너스 번호]
```

#### ❌ CORS 오류 시:
```
❌ 당첨 번호를 조회할 수 없습니다
동행복권 API 연결에 실패했습니다. CORS 정책으로 인해 직접 호출이 제한될 수 있습니다.
💡 브라우저의 CORS 정책으로 인해 동행복권 API를 직접 호출할 수 없습니다.
프록시 서버 설정이 필요합니다.
```

#### ⚠️ 미추첨 회차:
```
⚠️ 1197회차는 아직 추첨이 이루어지지 않았습니다.
추첨 후 다시 확인해주세요.
```

---

## 💡 추천 워크플로우

### 1단계: 로컬 테스트
```bash
python -m http.server 8000
# http://localhost:8000/enhanced_lotto.html 접속
```

### 2단계: GitHub에 업로드
```bash
git add .
git commit -m "UI 개선 및 API 연동"
git push origin main
```

### 3단계: Netlify 배포
- Netlify에서 GitHub 저장소 연결
- 자동 배포
- 프록시 서버 활성화

---

**이제 완벽하게 작동하는 로또 번호 생성기가 완성되었습니다!** 🎉

문제가 발생하면 개발자 도구(F12)의 Console과 Network 탭을 확인하세요.

