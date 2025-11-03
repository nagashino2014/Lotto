# GitHub Actions 자동 업데이트 가이드

## 🤖 자동 업데이트 시스템

GitHub Actions를 사용하여 **매주 일요일 오후 10시**에 자동으로 최신 로또 데이터를 업데이트합니다.

### ✅ 설정 완료 사항

1. **`.github/workflows/update-lotto.yml`** - GitHub Actions 워크플로우
2. **`scripts/update_lotto_weekly.py`** - 주간 업데이트 스크립트
3. **`scripts/download_all_lotto.py`** - 전체 데이터 다운로드 스크립트

---

## 📅 자동 업데이트 스케줄

- **매주 일요일 오후 10시 (KST)**
- 토요일 밤 추첨 후 다음날 자동 업데이트
- 변경사항이 있을 때만 커밋

---

## 🚀 작동 방식

```
1. 매주 일요일 오후 10시
   ↓
2. GitHub Actions 자동 실행
   ↓
3. 동행복권 API에서 최신 회차 조회
   ↓
4. CSV 파일에 없는 회차 다운로드
   ↓
5. lotto_data.csv 업데이트
   ↓
6. 자동 커밋 & 푸시
   ↓
7. GitHub Pages 자동 배포 ✅
```

---

## 🔍 확인 방법

### 1. GitHub Actions 페이지
https://github.com/YOUR_USERNAME/Lotto/actions

- 최근 실행 기록 확인
- 성공/실패 상태 확인
- 로그 확인

### 2. 수동 실행
GitHub Actions 페이지에서:
1. **"Update Lotto Data"** 워크플로우 선택
2. **"Run workflow"** 버튼 클릭
3. **"Run workflow"** 확인

---

## 📝 워크플로우 상세

### 실행 조건
```yaml
on:
  schedule:
    - cron: '0 13 * * 0'  # 매주 일요일 UTC 13시 (KST 22시)
  workflow_dispatch:  # 수동 실행 가능
```

### 실행 단계
1. **Checkout repository** - 저장소 체크아웃
2. **Set up Python** - Python 3.11 설치
3. **Install dependencies** - requests 패키지 설치
4. **Download latest lotto data** - 최신 데이터 다운로드
5. **Check for changes** - 변경사항 확인
6. **Commit and push** - 변경사항 있을 시 커밋

---

## 🛠️ 수동 업데이트 방법

자동 업데이트를 기다리지 않고 즉시 업데이트하려면:

### 방법 1: GitHub Actions (권장)
1. GitHub 저장소 > **Actions** 탭
2. **"Update Lotto Data"** 선택
3. **"Run workflow"** > **"Run workflow"** 클릭

### 방법 2: 로컬에서 실행
```bash
# Python 설치 필요
pip install requests

# 주간 업데이트 (최신 회차만)
python scripts/update_lotto_weekly.py

# 커밋 & 푸시
git add lotto_data.csv
git commit -m "Manual update"
git push
```

---

## 📊 데이터 범위

### 현재 저장된 데이터
- **시작**: 1회차 (2002년 12월 07일)
- **최신**: 1196회차
- **총**: 1196개 회차

### 자동 업데이트
- 매주 새로운 회차가 자동으로 추가됩니다
- 과거 데이터는 그대로 유지됩니다

---

## ⚠️ 문제 해결

### Actions 실행 실패
**원인**: API 타임아웃, 네트워크 오류
**해결**: 수동으로 다시 실행

### 데이터가 업데이트되지 않음
**원인 1**: 아직 새 회차가 발표되지 않음
- 토요일 밤 8시 45분 추첨 후 발표
- 일요일 오후 10시까지 기다림

**원인 2**: API에서 데이터를 가져오지 못함
- 수동으로 재실행
- 로그 확인

### 중복 데이터
- 스크립트가 자동으로 중복 제거
- 걱정하지 않아도 됩니다

---

## 💡 커스터마이징

### 실행 시간 변경
`.github/workflows/update-lotto.yml` 파일에서:

```yaml
schedule:
  - cron: '0 13 * * 0'  # UTC 시간
```

**시간 계산**:
- KST = UTC + 9시간
- KST 22시 = UTC 13시
- 원하는 시간으로 변경 가능

**예시**:
- 매일 오전 6시 (KST): `cron: '0 21 * * *'`
- 매주 월요일 오전 9시: `cron: '0 0 * * 1'`

### 알림 추가
Slack, Discord 등으로 업데이트 알림을 받으려면:

```yaml
- name: Notify
  if: steps.check_changes.outputs.changed == 'true'
  run: |
    # Slack webhook 또는 Discord webhook 호출
```

---

## 📈 통계

### API 호출
- 주 1회: 1회차만 조회
- 월 4회: 약 4회차 조회
- 연 52회: 약 52회차 조회

### GitHub Actions 사용량
- 실행 시간: 약 1-2분
- 무료 플랜: 월 2,000분
- 충분히 여유있음 ✅

---

## 🎉 자동화 완료!

이제 할 일:
- ✅ 자동 업데이트 설정 완료
- ✅ GitHub Actions 활성화
- ✅ 매주 일요일 자동 실행
- ✅ 더 이상 수동 작업 불필요!

**편하게 앱을 사용하세요!** 🚀

