# 🔧 권한 부족 (403) 오류 해결 가이드

## ❌ 발생하는 오류
```
저장 실패: ... 
❌ 권한이 부족합니다.
✅ Token 권한 확인:
- Contents: Read and write
- Repository: Lotto 선택됨
```

## 🎯 해결 방법 체크리스트

### ✅ 1. Fine-grained Token 설정 확인

GitHub에서 토큰 설정을 다시 확인하세요:

1. **GitHub 로그인** → 우측 상단 프로필 클릭
2. **Settings** 클릭
3. 좌측 맨 아래 **Developer settings** 클릭
4. **Personal access tokens** → **Fine-grained tokens** 클릭
5. 생성한 토큰 옆의 **... (점 3개)** 클릭 → **Edit** 선택

#### 필수 확인 사항:

**Repository access 섹션:**
```
◉ Only select repositories
  └─ Selected repositories:
      ✅ nagashino2014/Lotto  ← 이렇게 표시되어야 함!
```

**Repository permissions 섹션:**
```
Contents:
  Access: Read and write ✅
  
Metadata:
  Access: Read-only (mandatory) ✅
```

**⚠️ 중요:** 
- Repository access에서 **정확히 "Lotto" 저장소가 체크되어 있어야 합니다!**
- 만약 체크되어 있지 않다면, 이것이 문제의 원인입니다.

---

### ✅ 2. 브라우저 캐시 완전 삭제

이전 코드가 캐시되어 있을 수 있습니다:

**Chrome/Edge:**
1. `Ctrl + Shift + Delete` 누르기
2. **시간 범위**: "전체 기간" 선택
3. **캐시된 이미지 및 파일** 체크
4. **데이터 삭제** 클릭
5. 브라우저 완전히 닫고 재시작
6. `enhanced_lotto.html` 다시 열기

**또는 시크릿/프라이빗 모드에서 테스트:**
- `Ctrl + Shift + N` (시크릿 모드)
- `enhanced_lotto.html` 열기
- 토큰 입력 후 테스트

---

### ✅ 3. 토큰 형식 확인

**올바른 토큰 형식:**
```
github_pat_11ABCDEFG0123456789_abcdefghijklmnopqrstuvwxyz...
```

**확인 사항:**
- ✅ `github_pat_`로 시작하는지 확인
- ✅ 복사할 때 공백이나 줄바꿈이 포함되지 않았는지 확인
- ✅ 전체 토큰이 복사되었는지 확인 (매우 긴 문자열)

**재입력 방법:**
1. 토큰 입력란을 완전히 비우기
2. GitHub에서 토큰 다시 복사
3. 붙여넣기 후 앞뒤 공백 확인
4. 저장 후 다시 테스트

---

### ✅ 4. 저장소 이름 및 사용자명 확인

**앱의 "저장 관리" 탭에서:**
```
GitHub Personal Access Token: github_pat_...
사용자명: nagashino2014  ← 정확한 사용자명
저장소명: Lotto           ← 정확한 저장소명 (대소문자 구분!)
```

**GitHub에서 확인:**
1. `https://github.com/nagashino2014` 접속
2. `Lotto` 저장소가 존재하는지 확인
3. 저장소 이름이 정확히 `Lotto`인지 확인 (대소문자 구분!)

---

### ✅ 5. 토큰 재생성 (가장 확실한 방법)

설정을 다시 확인했는데도 안 되면, 토큰을 완전히 새로 만드세요:

#### 단계별 가이드:

**1. 기존 토큰 삭제:**
- GitHub → Settings → Developer settings → Fine-grained tokens
- 기존 토큰 옆 **...** → **Delete** 클릭

**2. 새 토큰 생성:**
- **Generate new token** 클릭

**3. 기본 정보 입력:**
```
Token name: Lotto App Token v2
Expiration: 90 days
Description: 로또 번호 저장용 (재생성)
```

**4. Repository access (⚠️ 매우 중요!):**
```
◉ Only select repositories  ← 이것을 선택!

[Select repositories] 버튼 클릭

검색창에 "Lotto" 입력

☑ nagashino2014/Lotto  ← 이 체크박스를 반드시 체크!
```

**5. Repository permissions:**
```
📦 Repository permissions (아래로 스크롤)

Contents 찾기
  └─ Access 드롭다운 클릭
      └─ "Read and write" 선택 ✅

Metadata (자동으로 Read-only로 설정됨)
```

**6. 생성 및 복사:**
```
- 페이지 맨 아래 [Generate token] 클릭
- 생성된 토큰 전체를 복사 (한 번만 표시됨!)
- 안전한 곳에 보관
```

**7. 앱에서 테스트:**
```
- enhanced_lotto.html 열기
- 저장 관리 탭
- 새 토큰 입력
- 테스트
```

---

### ✅ 6. GitHub API 요청 확인 (고급)

개발자 도구로 정확한 문제 파악:

**방법:**
1. `F12` → **Network** 탭
2. "저장" 버튼 클릭
3. `api.github.com` 요청 찾기
4. 클릭 후 확인:

**Headers 탭 확인:**
```
Request Headers:
  Authorization: Bearer github_pat_...  ← Bearer가 있는지 확인!
  Accept: application/vnd.github+json
  X-GitHub-Api-Version: 2022-11-28
```

만약 `Authorization: token github_pat_...`으로 표시되면:
→ **브라우저 캐시 문제!** 캐시를 완전히 삭제하고 재시작

**Response 탭 확인:**
```json
{
  "message": "Resource not accessible by personal access token",
  "documentation_url": "..."
}
```

이 메시지가 나오면:
→ **Repository가 선택되지 않았을 가능성이 높음!**

---

### ✅ 7. 저장소 타입 확인

**Public vs Private:**

- **Public 저장소**: Contents + Metadata 권한만 필요
- **Private 저장소**: 추가 권한이 필요할 수 있음

**확인 방법:**
1. `https://github.com/nagashino2014/Lotto` 접속
2. 저장소 이름 옆에 **Public** 또는 **Private** 표시 확인

**Private인 경우 추가 권한:**
Fine-grained token 설정에서 확인:
```
Repository permissions:
  ✅ Contents: Read and write
  ✅ Metadata: Read-only
```

---

### ✅ 8. Organization 저장소인 경우

만약 Lotto 저장소가 Organization에 속해 있다면:

1. Organization 관리자에게 Fine-grained token 사용 승인 요청
2. 또는 Classic token 사용 (덜 안전하지만 작동함)

**Classic Token 생성 (대안):**
1. GitHub → Settings → Developer settings
2. Personal access tokens → **Tokens (classic)**
3. Generate new token (classic)
4. **repo** 권한 전체 체크
5. Generate token
6. 복사 후 앱에서 사용

---

## 🎯 가장 흔한 원인 TOP 3

### 1위: Repository가 선택되지 않음 ⚠️
```
Fine-grained token 설정에서
"Only select repositories"를 선택했지만
실제로 "Lotto" 저장소를 체크하지 않은 경우!
```

**해결:** Token 편집 → Select repositories에서 Lotto 체크

### 2위: 브라우저 캐시 ⚠️
```
이전 버전의 코드가 캐시되어
token 방식이 아닌 Bearer 방식으로 전송되지 않음
```

**해결:** 브라우저 캐시 완전 삭제 + 재시작

### 3위: 토큰 복사 오류 ⚠️
```
토큰 복사 시 일부만 복사되거나
공백이 포함되어 있음
```

**해결:** 토큰 재복사 후 재입력

---

## 📞 여전히 안 되는 경우

다음 정보를 제공해주시면 더 정확히 도와드릴 수 있습니다:

1. **정확한 오류 메시지** (개발자 도구 Response 탭)
2. **토큰 형식** (앞 20자만: `github_pat_11ABCDEF...`)
3. **저장소 타입** (Public/Private)
4. **브라우저 종류 및 버전**
5. **Request Headers** (개발자 도구에서 Authorization 헤더 형식)

---

## ✅ 테스트 성공 확인

다음 메시지가 표시되면 성공입니다:
```
✅ [회차]회차 번호가 성공적으로 저장되었습니다!
```

그리고 GitHub에서 확인:
```
https://github.com/nagashino2014/Lotto
→ lotto_[회차]_[타임스탬프].json 파일이 생성됨
```

---

**대부분의 경우 Repository 선택 누락이나 브라우저 캐시 문제입니다!**
위의 1-3번 단계를 먼저 시도해보세요! 🚀

