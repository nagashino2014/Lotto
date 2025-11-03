# 자동 업데이트 시스템 가이드

## 🤖 GitHub Actions 자동화

이 프로젝트는 **매주 일요일 오후 10시**에 자동으로 최신 로또 데이터를 업데이트합니다.

### ✅ 설정 완료 항목

1. **GitHub Actions 워크플로우**: `.github/workflows/update-lotto.yml`
   - 매주 일요일 13:00 UTC (한국시간 22:00) 자동 실행
   - 수동 실행도 가능

2. **자동 업데이트 스크립트**: `scripts/update_lotto_data.py`
   - 동행복권 API에서 최신 회차 데이터 자동 다운로드
   - CSV 파일에 자동 추가
   - Git 자동 커밋 및 푸시

3. **전체 데이터**: `lotto_data.csv`
   - 1회 ~ 1196회 (2002.12.07 ~ 2024.11.09)
   - 총 1196개 회차 데이터

---

## 📅 자동 업데이트 일정

| 요일 | 시각 (KST) | 작업 |
|------|-----------|------|
| 토요일 | 20:45 | 로또 추첨 |
| 일요일 | 22:00 | **자동 데이터 업데이트** ✨ |

---

## 🔧 수동 실행 방법

### 방법 1: GitHub 웹에서 실행

1. GitHub 저장소 접속
2. `Actions` 탭 클릭
3. `Update Lotto Data` 워크플로우 선택
4. `Run workflow` 버튼 클릭
5. `Run workflow` 확인

### 방법 2: 로컬에서 실행

```bash
# 최신 회차만 업데이트
python scripts/update_lotto_data.py

# Git 커밋 & 푸시
git add lotto_data.csv
git commit -m "Update lotto data"
git push
```

### 방법 3: 전체 재다운로드 (필요시)

```bash
# 1회부터 최신 회차까지 모두 재다운로드
python scripts/download_all_lotto_data.py

# Git 커밋 & 푸시
git add lotto_data.csv
git commit -m "Re-download all lotto data"
git push
```

---

## 📊 작동 원리

### 자동 업데이트 프로세스

```
1. GitHub Actions 스케줄 트리거
   ↓
2. Python 스크립트 실행
   ↓
3. 동행복권 API에서 최신 회차 조회
   ↓
4. CSV 파일에 새 데이터 추가
   ↓
5. 변경사항이 있으면 자동 커밋
   ↓
6. GitHub에 자동 푸시
   ↓
7. GitHub Pages 자동 재배포 ✅
```

### API 호출 최적화

- **기존 최대 회차 확인**: CSV에서 마지막 회차 읽기
- **증분 업데이트**: 새 회차만 다운로드
- **API 부하 관리**: 요청 간 1초 대기
- **실패 처리**: 오류 발생 시 재시도 없이 종료

---

## 🔍 로그 확인

### GitHub Actions 로그 보기

1. GitHub 저장소 → `Actions` 탭
2. 최근 실행 내역 클릭
3. `update-lotto-data` 작업 로그 확인

**예시 로그**:
```
[LOTTO] 자동 업데이트 시작
[INFO] 실행 시각: 2024-11-17 13:00:00
[INFO] 현재 최대 회차: 1195회
[OK] 최신 회차 확인: 1196회
[OK] 1196회차 데이터 가져오는 중...
   [OK] 번호: 5, 12, 23, 29, 34, 41 + 18
[DONE] 업데이트 완료!
[INFO] 추가된 회차: 1개
[INFO] 총 회차: 1196개
```

---

## 🚨 문제 해결

### 자동 업데이트가 실행되지 않음

**원인**:
- GitHub Actions가 비활성화됨
- 워크플로우 파일 오류

**해결**:
1. GitHub 저장소 → `Settings` → `Actions` → `General`
2. `Allow all actions and reusable workflows` 선택
3. `.github/workflows/update-lotto.yml` 파일 문법 확인

### 업데이트는 되지만 커밋이 안됨

**원인**:
- 데이터 변경사항 없음 (이미 최신 상태)

**확인**:
```bash
git log --oneline
# 최근 커밋에 "Auto-update" 있는지 확인
```

### API 호출 실패

**원인**:
- 동행복권 사이트 점검
- 네트워크 오류

**해결**:
- 1시간 후 수동 재실행
- 동행복권 사이트 상태 확인

---

## 📈 통계

### CSV 파일 정보

- **파일 크기**: 약 100KB
- **회차 수**: 1196개
- **날짜 범위**: 2002.12.07 ~ 2024.11.09
- **업데이트 주기**: 주 1회 (일요일)

### GitHub Actions 사용량 (무료)

- **월 실행 횟수**: ~4회
- **실행 시간**: 회당 약 30초
- **무료 한도**: 2,000분/월
- **사용량**: 약 2분/월 (0.1% 사용)

---

## 🎯 향후 개선 계획

### Phase 1 (현재) ✅
- [x] GitHub Actions 자동화
- [x] 매주 일요일 자동 업데이트
- [x] 전체 회차 데이터 (1~1196회)

### Phase 2 (선택사항)
- [ ] Slack/Discord 알림 (업데이트 완료 시)
- [ ] 업데이트 실패 시 이메일 알림
- [ ] 당첨금 통계 자동 생성

### Phase 3 (고급)
- [ ] 동행복권 엑셀 파일 직접 파싱
- [ ] 여러 복권 게임 지원 (연금복권 등)
- [ ] 번호 분석 및 통계 자동 생성

---

## 💡 팁

1. **즉시 확인**: 업데이트 후 `lotto_data.csv` 파일 확인
2. **수동 실행**: 급하면 GitHub Actions에서 수동 실행
3. **로그 확인**: 실패 시 Actions 탭에서 오류 로그 확인
4. **백업**: Git 히스토리가 자동 백업 역할

---

## 📞 지원

문제 발생 시:
1. GitHub Issues에 등록
2. Actions 로그 첨부
3. 오류 메시지 복사

**즐거운 로또 생활 되세요!** 🍀

