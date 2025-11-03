# 🚀 로컬 웹 서버로 CORS 문제 해결하기

## ❌ 문제: CORS 오류 발생

로컬에서 `enhanced_lotto.html` 파일을 직접 더블클릭하여 열면 CORS(Cross-Origin Resource Sharing) 정책으로 인해 동행복권 API를 호출할 수 없습니다.

**오류 메시지:**
```
Access to fetch at 'https://www.dhlottery.co.kr/...' from origin 'null' 
has been blocked by CORS policy
```

---

## ✅ 해결책: 로컬 웹 서버 실행

로컬 웹 서버를 실행하면 `http://localhost` 도메인에서 파일을 서빙하므로 CORS 문제가 해결됩니다.

---

## 🎯 방법 1: Python 웹 서버 (가장 간단!)

### Windows/Mac/Linux 모두 가능

Python은 대부분의 컴퓨터에 기본 설치되어 있습니다.

#### 1. 터미널/명령 프롬프트 열기:
- **Windows**: `Win + R` → `cmd` 입력 → Enter
- **Mac**: `Cmd + Space` → "Terminal" 검색
- **Linux**: `Ctrl + Alt + T`

#### 2. 프로젝트 폴더로 이동:
```bash
cd C:\Users\nagas\OneDrive\문서\CodingProject\로또\Lotto
```

#### 3. Python 웹 서버 실행:

**Python 3 사용 (권장):**
```bash
python -m http.server 8000
```

**또는 Python 2 사용:**
```bash
python -m SimpleHTTPServer 8000
```

#### 4. 브라우저에서 접속:
```
http://localhost:8000/enhanced_lotto.html
```

#### 5. 사용 완료 후 서버 종료:
터미널에서 `Ctrl + C` 누르기

---

## 🎯 방법 2: Node.js 웹 서버

Node.js가 설치되어 있다면 이 방법도 사용 가능합니다.

#### 1. http-server 설치 (최초 1회만):
```bash
npm install -g http-server
```

#### 2. 프로젝트 폴더로 이동:
```bash
cd C:\Users\nagas\OneDrive\문서\CodingProject\로또\Lotto
```

#### 3. 웹 서버 실행:
```bash
http-server -p 8000
```

#### 4. 브라우저에서 접속:
```
http://localhost:8000/enhanced_lotto.html
```

---

## 🎯 방법 3: VS Code Live Server

VS Code를 사용 중이라면 가장 편리한 방법입니다.

#### 1. VS Code에서 프로젝트 폴더 열기

#### 2. Live Server 확장 설치:
- 좌측 Extensions 아이콘 클릭
- "Live Server" 검색
- "Install" 클릭

#### 3. enhanced_lotto.html 파일 열기

#### 4. 우클릭 → "Open with Live Server" 선택

#### 5. 자동으로 브라우저가 열림!
```
http://127.0.0.1:5500/enhanced_lotto.html
```

---

## 🎯 방법 4: Chrome 브라우저 확장 프로그램

간단하게 CORS를 우회할 수 있지만, **보안상 위험**하므로 테스트용으로만 사용하세요!

#### 1. Chrome Web Store에서 설치:
- "Allow CORS: Access-Control-Allow-Origin" 확장 프로그램 검색
- 설치

#### 2. 확장 프로그램 활성화:
- 브라우저 우측 상단의 확장 프로그램 아이콘 클릭
- "ON" 상태로 변경

#### 3. enhanced_lotto.html 파일 열기

#### 4. ⚠️ 사용 후 반드시 비활성화!

---

## 📊 각 방법 비교

| 방법 | 설치 필요 | 난이도 | 속도 | 권장도 |
|------|----------|--------|------|--------|
| **Python 서버** | ❌ (대부분 기본 설치) | ⭐ 쉬움 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Node.js 서버** | ✅ (Node.js + http-server) | ⭐⭐ 보통 | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| **VS Code Live Server** | ✅ (VS Code + 확장) | ⭐ 쉬움 | ⚡⚡⚡⚡ | ⭐⭐⭐⭐⭐ |
| **Chrome 확장** | ✅ (확장 프로그램) | ⭐ 매우 쉬움 | ⚡⚡⚡⚡ | ⭐⭐ (보안 위험) |

---

## 🎉 테스트 방법

로컬 웹 서버를 실행한 후:

1. **브라우저에서 접속**
   ```
   http://localhost:8000/enhanced_lotto.html
   ```

2. **당첨 체크 탭으로 이동**

3. **회차 번호 입력** (예: 1100)

4. **"🔍 당첨 확인" 버튼 클릭**

5. **개발자 도구 확인** (F12 → Console)
   - CORS 오류가 없어야 함!
   - 당첨번호가 정상적으로 표시되어야 함

---

## 💡 Python이 설치되어 있는지 확인하는 방법

터미널에서 다음 명령어 실행:

```bash
python --version
```

또는

```bash
python3 --version
```

**결과 예시:**
```
Python 3.11.5
```

만약 "python을 찾을 수 없습니다" 오류가 나오면:
1. https://www.python.org/downloads/ 에서 Python 다운로드
2. 설치 시 "Add Python to PATH" 체크박스 선택!
3. 설치 완료 후 터미널 재시작

---

## 🚀 빠른 시작 (복사 & 붙여넣기)

### Windows 사용자:
```cmd
cd C:\Users\nagas\OneDrive\문서\CodingProject\로또\Lotto
python -m http.server 8000
```

그 후 브라우저에서:
```
http://localhost:8000/enhanced_lotto.html
```

---

## ❓ 자주 묻는 질문

### Q: 포트 8000이 이미 사용 중이라고 나와요
**A:** 다른 포트 번호를 사용하세요:
```bash
python -m http.server 8080
```
그 후 `http://localhost:8080/enhanced_lotto.html` 접속

### Q: 서버를 종료하려면?
**A:** 터미널에서 `Ctrl + C` 누르기

### Q: 서버가 백그라운드에서 계속 실행되나요?
**A:** 아니요, 터미널을 닫으면 서버도 자동 종료됩니다.

### Q: 다른 컴퓨터에서도 접속할 수 있나요?
**A:** 같은 네트워크에 있다면 가능합니다. 
내 컴퓨터의 IP 주소를 확인 후 `http://[내 IP]:8000/enhanced_lotto.html` 접속

내 IP 확인 방법:
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

---

## 🌐 더 좋은 방법: Netlify 배포

로컬 웹 서버는 테스트용으로는 좋지만, 실제로 사용하려면 **Netlify에 배포**하는 것을 추천합니다!

### 장점:
- ✅ 어디서든 접속 가능
- ✅ HTTPS 자동 적용
- ✅ 무료!
- ✅ GitHub와 자동 연동
- ✅ Netlify Functions로 CORS 문제 완전 해결

### 배포 방법:
1. https://netlify.com 접속
2. GitHub 계정으로 로그인
3. "New site from Git" 클릭
4. "Lotto" 저장소 선택
5. Deploy!

그러면 다음과 같은 URL을 받게 됩니다:
```
https://your-site-name.netlify.app/enhanced_lotto.html
```

---

**이제 CORS 문제 없이 당첨번호를 확인할 수 있습니다!** 🎉

문제가 계속되면 `CORS_SOLUTION.md` 파일을 참고하세요.

