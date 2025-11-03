# 🔐 GitHub Fine-grained Personal Access Token 설정 가이드

## 문제 해결 완료! ✅

**"Resource not accessible by personal access token"** 오류가 이제 해결되었습니다!

## 📝 변경 사항

`enhanced_lotto.html` 파일을 수정하여 **Fine-grained personal access token**을 지원하도록 업데이트했습니다:

### 주요 변경 내용:
1. **인증 헤더 형식 변경**: `token` → `Bearer` 방식으로 변경
2. **GitHub API 버전 명시**: 최신 API 버전(2022-11-28) 사용
3. **Accept 헤더 추가**: GitHub API v3 표준 준수

## 🎯 Fine-grained Token 생성 방법

### 1단계: GitHub에서 토큰 생성

1. **GitHub 로그인** 후 우측 상단 프로필 클릭
2. **Settings** 선택
3. 좌측 메뉴에서 **Developer settings** 클릭
4. **Personal access tokens** → **Fine-grained tokens** 선택
5. **Generate new token** 버튼 클릭

### 2단계: 토큰 설정

다음과 같이 설정하세요:

#### 기본 정보
- **Token name**: `Lotto App Token` (원하는 이름)
- **Expiration**: 90일 또는 Custom (원하는 기간)
- **Description**: `로또 번호 생성기 앱용 토큰`

#### Repository access (중요! ⚠️)
- **Only select repositories** 선택
- **Select repositories** 클릭하여 `Lotto` 저장소 선택
  - 만약 저장소가 없다면, 먼저 GitHub에 `Lotto` 저장소를 생성하세요

#### Repository permissions (중요! ⚠️)
**Contents** 항목에서:
- **Access**: `Read and write` 선택
  
**Metadata** 항목:
- 자동으로 `Read-only`로 설정됨 (필수 권한)

### 3단계: 토큰 생성 및 복사

1. 페이지 하단의 **Generate token** 버튼 클릭
2. 생성된 토큰을 **반드시 복사**하여 안전한 곳에 보관
   - ⚠️ 이 토큰은 다시 볼 수 없으므로 즉시 복사하세요!
   - 형식: `github_pat_XXXXXXXXXXXX...`

### 4단계: 로또 앱에서 토큰 사용

1. `enhanced_lotto.html` 파일을 브라우저에서 열기
2. **저장 관리** 탭으로 이동
3. **GitHub 설정** 섹션에서:
   - **GitHub Personal Access Token**: 복사한 토큰 붙여넣기
   - **사용자명**: GitHub 사용자명 입력 (예: nagashino2014)
   - **저장소명**: `Lotto` 입력

4. **번호 생성** 탭에서 로또 번호 생성
5. **GitHub 저장** 버튼 클릭하여 테스트

## ✅ 권한 확인 체크리스트

Fine-grained token이 다음 권한을 가지고 있는지 확인하세요:

- ✅ Repository: `Lotto` 선택됨
- ✅ Contents: **Read and write** 권한
- ✅ Metadata: **Read-only** 권한 (자동)

## 🔧 문제 해결

### 여전히 오류가 발생하는 경우:

#### 1. "Not Found" 오류
**원인**: 저장소가 존재하지 않거나 이름이 잘못됨  
**해결**: GitHub에서 `Lotto` 저장소가 생성되어 있는지 확인

#### 2. "Bad credentials" 오류
**원인**: 토큰이 잘못되었거나 만료됨  
**해결**: 새 토큰을 생성하고 다시 입력

#### 3. "Resource not accessible" 오류 (여전히 발생 시)
**원인**: 토큰 권한이 부족함  
**해결**: 
- Contents 권한이 **Read and write**로 설정되어 있는지 확인
- 올바른 저장소가 선택되어 있는지 확인

#### 4. 브라우저 캐시 문제
**해결**: 
- 브라우저 캐시를 삭제 (Ctrl + Shift + Delete)
- 페이지를 강제 새로고침 (Ctrl + F5)

## 💡 보안 팁

1. **토큰 저장**: 앱은 토큰을 브라우저의 로컬 스토리지에 저장합니다
2. **토큰 보호**: 토큰을 다른 사람과 공유하지 마세요
3. **정기 갱신**: 토큰을 정기적으로 갱신하는 것이 좋습니다
4. **최소 권한**: 필요한 최소한의 권한만 부여하세요

## 🆚 Classic Token vs Fine-grained Token

### Classic Token (이전 방식)
- ❌ 모든 저장소에 대한 광범위한 권한
- ❌ 세밀한 권한 제어 불가능
- ❌ 보안 위험이 더 높음

### Fine-grained Token (새 방식 - 권장) ✅
- ✅ 특정 저장소만 선택 가능
- ✅ 세밀한 권한 제어 가능
- ✅ 보안성이 더 높음
- ✅ 만료 기간 설정 가능

## 📞 추가 도움이 필요한 경우

문제가 계속되면 다음을 확인하세요:

1. `enhanced_lotto.html` 파일이 최신 버전인지 확인
2. 브라우저 개발자 도구(F12)의 Console 탭에서 오류 메시지 확인
3. Network 탭에서 GitHub API 요청/응답 확인

---

**이제 로또 번호를 안전하게 저장하고 관리할 수 있습니다!** 🎉

