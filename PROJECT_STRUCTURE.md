# 프로젝트 구조

## 📂 파일 구조

```
Lotto/
├── 📄 enhanced_lotto.html          # 메인 애플리케이션
├── 📊 lotto_data.csv                # 로또 데이터베이스 (1~1196회)
│
├── 📚 문서
│   ├── README.md                    # 프로젝트 소개 및 사용법
│   ├── GITHUB_ACTIONS_GUIDE.md      # 자동 업데이트 가이드
│   ├── GITHUB_TOKEN_GUIDE.md        # GitHub 토큰 생성 가이드
│   ├── CSV_UPDATE_GUIDE.md          # 수동 CSV 업데이트 가이드
│   └── NETLIFY_DEPLOY_SIMPLE.md     # Netlify 배포 가이드
│
├── 🤖 자동화
│   ├── .github/
│   │   └── workflows/
│   │       └── update-lotto.yml     # 주간 자동 업데이트
│   └── scripts/
│       ├── update_lotto_weekly.py   # 주간 업데이트 스크립트
│       ├── fast_download.py         # 빠른 전체 다운로드
│       └── download_all_lotto.py    # 전체 데이터 다운로드
│
└── 🚀 배포 (선택사항)
    ├── netlify.toml                 # Netlify 설정
    └── netlify/functions/
        ├── lotto-api.js             # 동행복권 API 프록시
        └── lotto-scraper.js         # 네이버 스크래핑

```

## 📝 주요 파일 설명

### 핵심 파일

#### `enhanced_lotto.html`
- 로또 번호 생성, 저장, 당첨 확인 기능
- CSV 기반 빠른 조회 (0.1초)
- GitHub Pages에서 바로 실행 가능

#### `lotto_data.csv`
- 1회차 ~ 1196회차 당첨 데이터
- 603개 회차 포함
- 매주 자동 업데이트

### 문서

#### `README.md`
- 프로젝트 소개
- 기능 설명
- 설치 및 사용법

#### `GITHUB_ACTIONS_GUIDE.md`
- GitHub Actions 자동 업데이트 설정
- 매주 일요일 22시 자동 실행
- 수동 실행 방법

#### `GITHUB_TOKEN_GUIDE.md`
- Fine-grained Token 생성 방법
- 권한 설정 가이드
- 문제 해결

#### `CSV_UPDATE_GUIDE.md`
- 수동 CSV 업데이트 방법
- 엑셀 다운로드 및 변환
- Python 스크립트 사용법

#### `NETLIFY_DEPLOY_SIMPLE.md`
- Netlify 배포 가이드 (선택사항)
- 5분 만에 배포하는 방법

### 스크립트

#### `scripts/update_lotto_weekly.py`
- GitHub Actions에서 사용
- 최신 회차만 다운로드
- 자동 커밋

#### `scripts/fast_download.py`
- 병렬 다운로드로 빠른 수집
- 1~1196회 전체 다운로드
- 2-3분 소요

#### `scripts/download_all_lotto.py`
- 순차 다운로드 (안전)
- 전체 회차 수집
- 약 10분 소요

### Netlify (선택사항)

#### `netlify.toml`
- Netlify 배포 설정
- Functions 디렉토리 지정

#### `netlify/functions/lotto-api.js`
- 동행복권 API 프록시
- CORS 우회

#### `netlify/functions/lotto-scraper.js`
- 네이버 검색 결과 스크래핑
- 동행복권 API 대체

---

## 🗑️ 정리된 파일 (2024-11-03)

### 삭제된 파일
- `lotto_*.json` (4개) - 테스트 파일
- `AUTO_UPDATE_GUIDE.md` - 중복 가이드
- `CORS_SOLUTION.md` - CSV 방식으로 불필요
- `FIX_SUMMARY.md` - 개발 중 임시 문서
- `LOCAL_SERVER_GUIDE.md` - CSV 방식으로 불필요
- `TROUBLESHOOTING_403.md` - CSV 방식으로 불필요
- `TEST_GUIDE.md` - 개발 중 임시 문서
- `UPDATE_SUMMARY.md` - 개발 중 임시 문서
- `DEPLOY.md` - 중복 가이드
- `NETLIFY_DEPLOY_GUIDE.md` - 중복 가이드
- `lotto-api-proxy.js` - Netlify Functions로 대체
- `scripts/download_all_lotto_data.py` - 중복 스크립트
- `scripts/update_lotto_data.py` - 중복 스크립트

### 정리 이유
- CSV 방식 도입으로 CORS, API 문제 해결
- 중복 문서 제거
- 테스트 파일 정리
- 사용하지 않는 스크립트 제거

---

## 💡 파일 사용 가이드

### 일반 사용자
**필수**:
- `enhanced_lotto.html` - 앱 실행
- `lotto_data.csv` - 데이터

**참고**:
- `README.md` - 사용법

### 관리자
**자동 업데이트**:
- `.github/workflows/update-lotto.yml`
- `scripts/update_lotto_weekly.py`
- `GITHUB_ACTIONS_GUIDE.md`

**수동 업데이트**:
- `scripts/fast_download.py`
- `CSV_UPDATE_GUIDE.md`

### 개발자
**배포**:
- `netlify.toml`
- `netlify/functions/`
- `NETLIFY_DEPLOY_SIMPLE.md`

**토큰 설정**:
- `GITHUB_TOKEN_GUIDE.md`

---

## 🎯 권장 사항

### 사용자
1. `enhanced_lotto.html` 실행
2. GitHub Pages에서 사용 (권장)
3. 자동 업데이트로 항상 최신 데이터

### 관리자
1. GitHub Actions 활성화 (자동)
2. 문제 발생 시만 수동 개입
3. 주간 업데이트 로그 확인

### 개발자
1. CSV 방식 유지 (최고 성능)
2. Netlify는 선택사항
3. 코드 수정 시 테스트 필수

