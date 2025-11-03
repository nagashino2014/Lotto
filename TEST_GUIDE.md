# 🧪 수정 사항 테스트 가이드

## ✅ 빠른 테스트 절차

### 1단계: 브라우저 캐시 초기화 (중요!)
수정된 파일이 제대로 로드되도록 캐시를 삭제하세요:

**Chrome/Edge:**
1. `Ctrl + Shift + Delete` 누르기
2. "캐시된 이미지 및 파일" 선택
3. "데이터 삭제" 클릭
4. 또는 `enhanced_lotto.html` 페이지에서 `Ctrl + F5` (강제 새로고침)

**Firefox:**
1. `Ctrl + Shift + Delete` 누르기
2. "캐시" 선택
3. "지금 삭제" 클릭

### 2단계: GitHub 저장소 확인
1. GitHub에 로그인
2. `https://github.com/nagashino2014` (본인 계정으로 변경)으로 이동
3. `Lotto` 저장소가 있는지 확인
   - 없다면 **New repository** 클릭하여 생성
   - Repository name: `Lotto`
   - Public 또는 Private 선택 (둘 다 가능)
   - Create repository 클릭

### 3단계: Fine-grained Token 생성
1. GitHub → **Settings** (우측 상단 프로필 클릭)
2. 좌측 메뉴 맨 아래 **Developer settings** 클릭
3. **Personal access tokens** → **Fine-grained tokens** 선택
4. **Generate new token** 클릭

#### Token 설정:
```
Token name: Lotto App Token
Expiration: 90 days (권장)
Description: 로또 번호 생성기 앱용

Repository access:
  ✅ Only select repositories
  └─ Select repositories: Lotto

Repository permissions:
  ✅ Contents: Read and write
  ✅ Metadata: Read-only (자동 설정됨)
```

5. **Generate token** 클릭
6. 생성된 토큰을 **즉시 복사** (형식: `github_pat_...`)
   - ⚠️ 이 페이지를 벗어나면 다시 볼 수 없습니다!

### 4단계: 앱 테스트
1. `enhanced_lotto.html` 파일을 브라우저에서 열기
2. **저장 관리** 탭 클릭

#### 확인할 UI 요소:
- ✅ 파란색 안내 박스가 보이는지 확인:
  ```
  💡 Fine-grained Token 사용 권장
  Settings → Developer settings → Personal access tokens → Fine-grained tokens
  권한: Repository (Lotto) → Contents (Read and write)
  ```
- ✅ 토큰 입력란 플레이스홀더: `GitHub Personal Access Token (github_pat_...)`

3. GitHub 설정 입력:
   - **GitHub Personal Access Token**: 복사한 토큰 붙여넣기
   - **사용자명**: 본인의 GitHub 사용자명 (예: nagashino2014)
   - **저장소명**: `Lotto`

### 5단계: 번호 생성 및 저장 테스트
1. **번호 생성** 탭으로 이동
2. "생성할 조합 수" 선택 (5개 권장)
3. **🎲 번호 생성** 버튼 클릭
4. 번호가 생성되었는지 확인
5. **💾 GitHub 저장** 버튼 클릭

#### 모달창에서:
- **로또 회차 입력**: 예를 들어 `1200`
- **메모**: 예를 들어 `테스트`
- **저장** 버튼 클릭

### 6단계: 결과 확인

#### ✅ 성공 시:
```
✅ "1200회차 번호가 성공적으로 저장되었습니다!" 메시지가 표시됨
```

#### ❌ 실패 시 (404 오류):
```
❌ 저장소를 찾을 수 없습니다.
✅ GitHub에서 "Lotto" 저장소를 먼저 생성해주세요.
```
→ **해결**: 2단계로 돌아가서 저장소 생성

#### ❌ 실패 시 (403 오류):
```
❌ 권한이 부족합니다.
✅ Token 권한 확인:
- Contents: Read and write
- Repository: Lotto 선택됨
```
→ **해결**: 3단계로 돌아가서 토큰 재생성 (권한 확인)

#### ❌ 실패 시 (401 오류):
```
❌ 인증에 실패했습니다.
✅ 토큰이 올바른지 확인해주세요.
✅ Fine-grained token의 경우 만료되지 않았는지 확인하세요.
```
→ **해결**: 토큰을 다시 복사해서 붙여넣기

### 7단계: 저장된 번호 확인
1. **저장 관리** 탭으로 이동
2. **🔄 저장된 번호 불러오기** 버튼 클릭
3. 저장된 `1200회차` 항목이 표시되는지 확인
4. 항목을 클릭하면 번호가 표시되는지 확인

### 8단계: GitHub에서 직접 확인 (최종 검증)
1. `https://github.com/nagashino2014/Lotto` (본인 계정으로 변경)로 이동
2. `lotto_1200_...json` 파일이 생성되어 있는지 확인
3. 파일을 클릭하여 내용을 확인:
   ```json
   {
     "round": 1200,
     "date": "2025-11-03T...",
     "memo": "테스트",
     "numbers": [
       [1, 12, 23, 34, 40, 45],
       ...
     ]
   }
   ```

## 🎉 테스트 성공!

위의 모든 단계가 정상적으로 완료되면 수정이 성공적으로 적용된 것입니다!

## 🐛 문제가 계속되는 경우

### 개발자 도구로 디버깅:
1. `F12` 키를 눌러 개발자 도구 열기
2. **Console** 탭 확인:
   - 오류 메시지가 있는지 확인
3. **Network** 탭 확인:
   - "GitHub 저장" 버튼을 누른 후 Network 탭 관찰
   - `https://api.github.com/repos/...` 요청 찾기
   - 요청을 클릭하여 **Headers** 확인:
     ```
     Authorization: Bearer github_pat_...  ← 이렇게 되어있어야 함
     Accept: application/vnd.github+json
     X-GitHub-Api-Version: 2022-11-28
     ```
   - **Response** 탭에서 오류 메시지 확인

### 스크린샷 제공:
문제가 계속되면 다음 스크린샷을 제공해주세요:
1. 오류 메시지 알림창
2. 개발자 도구 Console 탭
3. 개발자 도구 Network 탭의 요청/응답

## 📝 체크리스트

테스트를 완료하면 체크하세요:

- [ ] 브라우저 캐시 삭제 완료
- [ ] GitHub에 `Lotto` 저장소 생성 확인
- [ ] Fine-grained Token 생성 완료
- [ ] 토큰 권한 확인 (Contents: Read and write)
- [ ] 앱에서 토큰 입력 완료
- [ ] 번호 생성 성공
- [ ] GitHub 저장 성공
- [ ] 저장된 번호 불러오기 성공
- [ ] GitHub에서 파일 확인 완료

---

**모든 테스트를 통과하면 수정이 완벽하게 적용된 것입니다!** 🎊

