# Netlify 배포 가이드

## 왜 Netlify를 사용해야 하나요?

GitHub Pages는 **정적 파일**만 호스팅하므로:
- ❌ 서버 사이드 기능 사용 불가
- ❌ CORS 프록시 필요 (불안정)
- ❌ 동행복권/네이버 API 직접 호출 차단

Netlify는 **서버리스 함수**를 지원하므로:
- ✅ Netlify Functions로 서버 사이드에서 API 호출
- ✅ CORS 문제 완전 해결
- ✅ 안정적이고 빠른 응답
- ✅ 무료 플랜으로 충분

---

## 🎯 간단 배포 (5분 소요)

### 1단계: Netlify 회원가입
1. https://www.netlify.com/ 접속
2. **Sign up** 클릭
3. **GitHub 계정으로 가입** (권장)

### 2단계: GitHub 저장소 연결
1. Netlify 대시보드에서 **Add new site** > **Import an existing project** 클릭
2. **Deploy with GitHub** 선택
3. `Lotto` 저장소 선택
4. 설정 확인:
   - **Branch to deploy**: `main`
   - **Build command**: (비워두기)
   - **Publish directory**: `.` (현재 디렉토리)
   - **Functions directory**: `netlify/functions` (자동 감지됨)
5. **Deploy site** 클릭

### 3단계: 배포 완료 대기
- 1-2분 정도 소요
- 배포 완료 후 자동으로 URL 생성 (예: `https://your-site-name.netlify.app`)

### 4단계: 사이트 접속
- 제공된 URL로 접속
- `enhanced_lotto.html` 파일 열기
- 이제 당첨 번호 조회가 완벽하게 작동합니다! 🎉

---

## 🔧 고급 설정 (선택사항)

### 커스텀 도메인 설정
1. Netlify 사이트 설정 > **Domain management**
2. **Add custom domain** 클릭
3. 도메인 입력 후 DNS 설정

### 환경 변수 설정
1. Site settings > **Environment variables**
2. GitHub Token 등 민감한 정보 저장 가능

### 자동 배포 설정
- GitHub에 push하면 자동으로 재배포됨
- Pull Request마다 미리보기 생성

---

## 📊 Netlify vs GitHub Pages 비교

| 기능 | GitHub Pages | Netlify |
|------|--------------|---------|
| 정적 호스팅 | ✅ | ✅ |
| 서버리스 함수 | ❌ | ✅ |
| CORS 우회 | ❌ | ✅ |
| 자동 배포 | ✅ | ✅ |
| 커스텀 도메인 | ✅ | ✅ |
| HTTPS | ✅ | ✅ |
| 빌드 제한 | - | 300분/월 (무료) |
| 대역폭 | 100GB/월 | 100GB/월 (무료) |

---

## 🐛 문제 해결

### "Functions not found" 오류
- `netlify.toml` 파일이 있는지 확인
- Functions 경로가 `netlify/functions`인지 확인

### 배포는 성공했지만 Functions 실행 안 됨
- 함수 로그 확인: Netlify 대시보드 > Functions
- 브라우저 콘솔에서 네트워크 탭 확인

### GitHub 연동 문제
- Netlify에 GitHub 권한 부여 확인
- 저장소가 Public인지 확인

---

## 💡 팁

1. **사이트 이름 변경**: Site settings > **Change site name**
2. **빌드 로그 확인**: Deploys > 최신 배포 클릭
3. **Functions 테스트**: 
   ```
   https://your-site.netlify.app/.netlify/functions/lotto-scraper?round=1195
   ```

---

## 📞 도움말

- Netlify 공식 문서: https://docs.netlify.com/
- Functions 가이드: https://docs.netlify.com/functions/overview/

