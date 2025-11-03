# 🎯 로또 번호 생성기 Pro v2.0

## ⚠️ 중요: 배포 방법 선택

### 🎯 GitHub Pages (강력 권장)

- ✅ **완전 무료** (과금 없음)
- ✅ 당첨번호 조회 **완벽 작동** (CSV 방식)
- ✅ **0.1초 이내** 즉시 조회
- ✅ CORS 문제 **없음**
- ✅ 설정 **간단**
- ⚠️ 주 1회 CSV 업데이트 필요 (5분 소요)

👉 **지금 바로 사용 가능!**

### 🚀 Netlify 배포 (선택사항)

- ✅ 최신 회차 자동 조회
- ⚠️ 무료 크레딧 소진 시 과금 가능
- ⚠️ 설정 복잡

👉 **[Netlify 배포 가이드 보기](NETLIFY_DEPLOY_SIMPLE.md)**

---

## 📊 데이터 업데이트 방법

이 앱은 **CSV 파일 기반**으로 작동하여 빠르고 안정적입니다.

### 🤖 자동 업데이트 (권장)

**GitHub Actions**가 매주 일요일 오후 10시에 자동으로 업데이트합니다!

- ✅ **완전 자동**: 아무것도 할 필요 없음
- ✅ **매주 실행**: 토요일 추첨 다음날 자동 업데이트
- ✅ **무료**: GitHub Actions 무료 플랜 사용
- ✅ **안정적**: 실패 시 자동 재시도

👉 **[자동 업데이트 상세 가이드](GITHUB_ACTIONS_GUIDE.md)**

### 📊 현재 데이터

- **총 회차**: 603개 (1회 ~ 1196회)
- **시작**: 1회차 (2002년 12월 07일)
- **최신**: 1196회차 (2025년 11월 01일)
- **업데이트**: 매주 자동

### 🔧 수동 업데이트 (선택사항)

자동 업데이트를 기다리지 않으려면:

**방법 1: GitHub에서 직접**
1. GitHub 저장소 > **Actions** 탭
2. "Update Lotto Data" 워크플로우 선택
3. **"Run workflow"** 버튼 클릭

**방법 2: 로컬에서**
```bash
python scripts/update_lotto_weekly.py
git add lotto_data.csv
git commit -m "Manual update"
git push
```

👉 **[수동 업데이트 가이드](CSV_UPDATE_GUIDE.md)**

## 📌 주요 기능

### 1. 🎲 스마트 번호 생성

- 5개부터 100개까지 원하는 만큼 번호 조합 생성
- 완전 무작위 알고리즘으로 공정한 번호 생성
- 시각적으로 아름다운 번호 공 디스플레이

### 2. 💾 GitHub 저장 기능

- 생성한 번호 조합을 GitHub 저장소에 안전하게 보관
- 회차별로 구분하여 체계적인 관리
- 메모 기능으로 특별한 조합 표시

### 3. 🏆 당첨 확인 기능

- 저장된 번호와 실제 당첨 번호 자동 비교
- 당첨 등수별 정확한 판정
  - **1등**: 6개 번호 모두 일치
  - **2등**: 5개 번호 + 보너스 번호 일치
  - **3등**: 5개 번호 일치
  - **4등**: 4개 번호 일치
  - **5등**: 3개 번호 일치
- 예상 당첨금 계산

### 4. 📄 PDF 다운로드

- 생성한 번호를 PDF로 저장
- 인쇄하여 편리하게 보관

## 🚀 사용 방법

### 1. GitHub Pages에 호스팅하기

1. GitHub에 새 저장소 생성 (예: `Lotto`)
2. `enhanced_lotto.html` 파일을 저장소에 업로드
3. Settings → Pages에서 GitHub Pages 활성화
4. `https://[username].github.io/Lotto/enhanced_lotto.html`로 접속

### 2. GitHub Personal Access Token 생성 (Fine-grained 권장)

번호를 GitHub에 저장하려면 Personal Access Token이 필요합니다:

#### Fine-grained Token 생성 (권장 ✅)

1. GitHub 로그인 → Settings → Developer settings
2. Personal access tokens → **Fine-grained tokens** → Generate new token
3. 토큰 설정:
   - **Token name**: `Lotto App Token`
   - **Repository access**: Only select repositories → `Lotto` 선택
   - **Repository permissions**:
     - **Contents**: Read and write ✅
     - **Metadata**: Read-only (자동 설정)
4. Generate token 클릭 후 토큰 복사 (`github_pat_...` 형식)
5. 로또 생성기의 "저장 관리" 탭에 토큰 입력

#### Classic Token (대안)

1. Personal access tokens → Tokens (classic) → Generate new token
2. 권한 선택: `repo` (전체 선택)
3. Generate token 후 토큰 복사

📖 자세한 가이드는 `GITHUB_TOKEN_GUIDE.md` 파일을 참고하세요!

### 3. 실제 당첨 번호 조회 기능 활성화

CORS 정책으로 인해 브라우저에서 직접 동행복권 API를 호출할 수 없습니다.
실제 당첨 번호 조회를 위해서는 프록시 서버가 필요합니다.

#### 옵션 1: Netlify Functions 사용

`netlify/functions/lotto-api.js` 파일 생성:

```javascript
exports.handler = async (event) => {
  const round = event.queryStringParameters.round;

  try {
    const response = await fetch(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
    );
    const data = await response.json();

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        round: data.drwNo,
        date: `${data.drwNoDate}`,
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
          1: { count: data.firstPrzwnerCo, amount: data.firstWinamnt },
          2: { count: data.secondPrzwnerCo, amount: data.secondWinamnt },
          3: { count: data.thirdPrzwnerCo, amount: data.thirdWinamnt },
          4: { count: data.fourthPrzwnerCo, amount: data.fourthWinamnt },
          5: { count: data.fifthPrzwnerCo, amount: data.fifthWinamnt },
        },
      }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Failed to fetch lottery data" }),
    };
  }
};
```

#### 옵션 2: Vercel Functions 사용

`api/lotto.js` 파일 생성:

```javascript
export default async function handler(req, res) {
  const { round } = req.query;

  try {
    const response = await fetch(
      `https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=${round}`
    );
    const data = await response.json();

    res.status(200).json({
      round: data.drwNo,
      date: `${data.drwNoDate}`,
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
        1: { count: data.firstPrzwnerCo, amount: data.firstWinamnt },
        2: { count: data.secondPrzwnerCo, amount: data.secondWinamnt },
        3: { count: data.thirdPrzwnerCo, amount: data.thirdWinamnt },
        4: { count: data.fourthPrzwnerCo, amount: data.fourthWinamnt },
        5: { count: data.fifthPrzwnerCo, amount: data.fifthWinamnt },
      },
    });
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch lottery data" });
  }
}
```

### 4. HTML 파일 수정

프록시 서버를 설정한 후, `fetchWinningNumbers` 함수를 다음과 같이 수정:

```javascript
async function fetchWinningNumbers(round) {
  // Netlify 사용 시
  const response = await fetch(`/.netlify/functions/lotto-api?round=${round}`);

  // Vercel 사용 시
  // const response = await fetch(`/api/lotto?round=${round}`);

  if (!response.ok) {
    throw new Error("Failed to fetch winning numbers");
  }

  return await response.json();
}
```

## 📱 모바일 지원

- 반응형 디자인으로 모든 디바이스에서 완벽 작동
- 터치 친화적인 인터페이스
- 모바일에서도 PDF 다운로드 지원

## 🔒 보안

- GitHub Personal Access Token은 로컬 스토리지에 암호화되어 저장
- 모든 데이터는 사용자의 개인 GitHub 저장소에만 저장
- 제3자 서버를 거치지 않는 안전한 구조

## 🎨 UI/UX 특징

- 모던하고 세련된 그라데이션 디자인
- 부드러운 애니메이션 효과
- 직관적인 탭 인터페이스
- 당첨 등수별 컬러 코딩
- 다크모드 지원 (추후 업데이트 예정)

## 📊 통계 기능

- 생성한 번호 개수 추적
- 저장한 회차 수 기록
- 당첨 확인 횟수 표시

## 🆕 향후 업데이트 예정

- [ ] 번호 분석 기능 (자주 나오는 번호, 최근 트렌드)
- [ ] 당첨 히스토리 차트
- [ ] 번호 패턴 분석
- [ ] 친구와 번호 공유 기능
- [ ] PWA(Progressive Web App) 지원

## 📝 라이센스

MIT License - 자유롭게 사용, 수정, 배포 가능

## 🤝 기여하기

버그 리포트나 기능 제안은 Issues를 통해 제출해주세요!

---

**⚠️ 주의사항**: 이 도구는 엔터테인먼트 목적으로만 사용하세요.
로또는 확률 게임이며, 과도한 구매는 피해주세요. 책임감 있는 게임 문화를 만들어갑시다.
