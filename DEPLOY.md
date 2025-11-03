# 🚀 로또 번호 생성기 배포 가이드

## 📁 프로젝트 구조

```
Lotto/
├── enhanced_lotto.html     # 메인 웹 애플리케이션
├── README.md               # 프로젝트 설명서
├── netlify/
│   └── functions/
│       └── lotto-api.js    # Netlify Functions API 프록시
├── api/
│   └── lotto.js           # Vercel Functions API 프록시 (선택)
├── server.js              # 독립 Node.js 서버 (선택)
└── package.json           # Node.js 의존성 파일
```

## 🌐 배포 옵션

### 옵션 1: GitHub Pages (정적 호스팅)

가장 간단한 방법이지만, API 프록시 없이 기본 기능만 사용 가능합니다.

1. **GitHub 저장소 생성**
   ```bash
   git init
   git add enhanced_lotto.html README.md
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/nagashino2014/Lotto.git
   git push -u origin main
   ```

2. **GitHub Pages 활성화**
   - Repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, /(root)
   - Save

3. **접속 URL**
   ```
   https://nagashino2014.github.io/Lotto/enhanced_lotto.html
   ```

### 옵션 2: Netlify (무료 서버리스)

API 프록시와 함께 모든 기능을 사용할 수 있습니다.

1. **프로젝트 구조 설정**
   ```
   Lotto/
   ├── enhanced_lotto.html (index.html로 변경)
   ├── netlify/
   │   └── functions/
   │       └── lotto-api.js
   └── netlify.toml
   ```

2. **netlify.toml 파일 생성**
   ```toml
   [build]
     functions = "netlify/functions"

   [[redirects]]
     from = "/"
     to = "/index.html"
     status = 200
   ```

3. **Netlify 배포**
   - [Netlify](https://www.netlify.com) 가입
   - "Add new site" → "Import an existing project"
   - GitHub 저장소 연결
   - Deploy site

4. **HTML 파일 수정**
   ```javascript
   async function fetchWinningNumbers(round) {
       const response = await fetch(`/.netlify/functions/lotto-api?round=${round}`);
       if (!response.ok) {
           throw new Error('Failed to fetch winning numbers');
       }
       return await response.json();
   }
   ```

### 옵션 3: Vercel (무료 서버리스)

1. **프로젝트 구조**
   ```
   Lotto/
   ├── enhanced_lotto.html (index.html로 변경)
   ├── api/
   │   └── lotto.js
   └── vercel.json
   ```

2. **vercel.json 파일 생성**
   ```json
   {
     "functions": {
       "api/lotto.js": {
         "maxDuration": 10
       }
     }
   }
   ```

3. **Vercel 배포**
   - [Vercel](https://vercel.com) 가입
   - "New Project" → GitHub 저장소 선택
   - Deploy

### 옵션 4: 독립 서버 (VPS/Cloud)

완전한 제어가 필요한 경우 사용합니다.

1. **서버 준비 (Ubuntu/Debian)**
   ```bash
   # Node.js 설치
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # PM2 설치 (프로세스 관리)
   sudo npm install -g pm2
   ```

2. **프로젝트 배포**
   ```bash
   # 프로젝트 클론
   git clone https://github.com/nagashino2014/Lotto.git
   cd Lotto

   # 의존성 설치
   npm install

   # PM2로 서버 시작
   pm2 start server.js --name lotto-api
   pm2 save
   pm2 startup
   ```

3. **Nginx 설정 (리버스 프록시)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           root /var/www/lotto;
           index enhanced_lotto.html;
       }

       location /api {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

## 🔑 GitHub Personal Access Token 생성

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. 권한 설정:
   - `repo` (전체)
   - `write:packages` (선택사항)
5. Token 생성 및 안전하게 보관

## 🔧 환경 변수 설정

### Netlify
Dashboard → Site settings → Environment variables
```
GITHUB_TOKEN=your_github_token
```

### Vercel
Dashboard → Settings → Environment Variables
```
GITHUB_TOKEN=your_github_token
```

### 독립 서버
`.env` 파일 생성:
```
GITHUB_TOKEN=your_github_token
PORT=3000
```

## 📱 모바일 앱으로 설치 (PWA)

1. **manifest.json 파일 생성**
   ```json
   {
     "name": "로또 번호 생성기 Pro",
     "short_name": "로또 Pro",
     "description": "스마트한 로또 번호 생성 및 당첨 확인",
     "start_url": "/",
     "display": "standalone",
     "background_color": "#f5f7fa",
     "theme_color": "#4F46E5",
     "icons": [
       {
         "src": "icon-192.png",
         "sizes": "192x192",
         "type": "image/png"
       },
       {
         "src": "icon-512.png",
         "sizes": "512x512",
         "type": "image/png"
       }
     ]
   }
   ```

2. **HTML에 추가**
   ```html
   <link rel="manifest" href="/manifest.json">
   <meta name="apple-mobile-web-app-capable" content="yes">
   <meta name="apple-mobile-web-app-status-bar-style" content="default">
   ```

3. **Service Worker 추가 (선택)**
   ```javascript
   // sw.js
   self.addEventListener('install', event => {
     console.log('Service Worker installed');
   });

   self.addEventListener('fetch', event => {
     event.respondWith(
       caches.match(event.request)
         .then(response => response || fetch(event.request))
     );
   });
   ```

## 🔍 문제 해결

### CORS 오류
- API 프록시 서버가 제대로 설정되었는지 확인
- 헤더에 `Access-Control-Allow-Origin: *` 포함 확인

### GitHub 저장 실패
- Personal Access Token 권한 확인
- 저장소 이름과 사용자명 확인
- Token 만료 여부 확인

### 당첨번호 조회 실패
- 회차 번호가 유효한지 확인 (1~최신회차)
- API 서버 상태 확인
- 네트워크 연결 확인

## 🚨 보안 주의사항

1. **GitHub Token 보호**
   - 절대 HTML 코드에 직접 입력하지 마세요
   - 환경 변수 사용 권장
   - 정기적으로 토큰 갱신

2. **HTTPS 사용**
   - 모든 배포 환경에서 HTTPS 사용
   - Let's Encrypt 무료 인증서 활용

3. **Rate Limiting**
   - API 호출 횟수 제한 구현
   - 캐싱 활용

## 📞 지원 및 문의

- GitHub Issues: https://github.com/nagashino2014/Lotto/issues
- Email: your-email@example.com

## 📄 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

**마지막 업데이트**: 2024년 11월