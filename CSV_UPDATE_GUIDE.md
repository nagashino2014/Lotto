# 로또 데이터 CSV 업데이트 가이드

## 📊 왜 CSV 방식인가?

### ✅ 장점
- **무료**: Netlify 과금 걱정 없음
- **빠름**: 파일만 읽으면 되므로 0.1초 이내 조회
- **안정적**: API 차단, CORS 문제 없음
- **정확함**: 동행복권 공식 데이터
- **간단함**: GitHub Pages에서도 완벽 작동

### ⚠️ 단점
- 새 추첨 후 수동 업데이트 필요 (주 1회, 약 5분 소요)

---

## 🎯 업데이트 방법 (주 1회)

### 1단계: 엑셀 파일 다운로드

1. [동행복권 당첨결과 페이지](https://dhlottery.co.kr/gameResult.do?method=byWin) 접속
2. **엑셀 다운로드** 버튼 클릭
3. 조회 범위 설정:
   - 예: 1195회 ~ 1195회 (최신 회차만)
   - 또는 여러 회차 한번에: 1180회 ~ 1195회
4. **다운로드** 클릭

### 2단계: 엑셀을 CSV로 변환

**방법 A: 엑셀 프로그램 사용**
1. 다운로드한 엑셀 파일 열기
2. 필요한 열만 선택:
   - 회차, 추첨일, 번호1~6, 보너스, 1등 당첨금, 2등 당첨금, 3등 당첨금
3. `다른 이름으로 저장` → `CSV UTF-8` 선택
4. 파일명: `lotto_new.csv`

**방법 B: Google Sheets 사용**
1. Google Sheets에서 엑셀 파일 열기
2. `파일` → `다운로드` → `쉼표로 구분된 값(.csv)`

**방법 C: Python 스크립트 (자동화)**
```python
import pandas as pd

# 엑셀 파일 읽기
df = pd.read_excel('lotto_download.xlsx')

# 필요한 열만 선택
df_clean = df[['회차', '추첨일', '번호1', '번호2', '번호3', '번호4', '번호5', '번호6', '보너스', '1등당첨금', '2등당첨금', '3등당첨금']]

# 열 이름 변경
df_clean.columns = ['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3']

# CSV로 저장
df_clean.to_csv('lotto_new.csv', index=False, encoding='utf-8')
print('✅ CSV 변환 완료!')
```

### 3단계: CSV 파일 형식 확인

**올바른 형식**:
```csv
round,date,num1,num2,num3,num4,num5,num6,bonus,prize1,prize2,prize3
1195,2024.11.02,3,15,27,33,34,36,37,2543995270,71221852,1581291
1194,2024.10.26,10,13,21,26,32,44,20,2472363950,69233176,1538960
```

**주의사항**:
- 첫 줄은 헤더 (round,date,num1,...)
- 날짜 형식: YYYY.MM.DD
- 당첨금은 쉼표 없이 숫자만 (2543995270)

### 4단계: 기존 CSV에 추가

**옵션 A: 파일 직접 편집**
1. `lotto_data.csv` 파일 열기
2. 새 회차 데이터를 **두 번째 줄**에 추가 (최신이 위로)
3. 저장

**옵션 B: 명령줄 (Windows)**
```cmd
type lotto_new.csv >> lotto_data.csv
```

**옵션 C: Python 스크립트**
```python
import pandas as pd

# 기존 데이터 로드
existing = pd.read_csv('lotto_data.csv')
new_data = pd.read_csv('lotto_new.csv')

# 병합 (중복 제거)
combined = pd.concat([new_data, existing]).drop_duplicates(subset=['round'], keep='first')

# 회차 내림차순 정렬
combined = combined.sort_values('round', ascending=False)

# 저장
combined.to_csv('lotto_data.csv', index=False)
print('✅ 병합 완료!')
```

### 5단계: GitHub에 커밋

```bash
git add lotto_data.csv
git commit -m "Update: Add lotto round 1195 data"
git push origin main
```

---

## 🤖 자동화 스크립트 (권장)

`update_lotto_csv.py` 파일 생성:

```python
#!/usr/bin/env python3
"""
로또 CSV 업데이트 자동화 스크립트
사용법: python update_lotto_csv.py lotto_download.xlsx
"""

import sys
import pandas as pd

def update_lotto_csv(excel_file):
    print(f'📂 {excel_file} 읽는 중...')
    
    # 엑셀 파일 읽기
    df = pd.read_excel(excel_file)
    
    # 필요한 열만 선택 (실제 열 이름에 맞게 수정 필요)
    required_cols = ['회차', '추첨일', '번호1', '번호2', '번호3', '번호4', '번호5', '번호6', '보너스']
    
    # 당첨금 열 찾기
    prize_cols = [col for col in df.columns if '당첨금' in col or '당첨' in col]
    
    df_clean = df[required_cols + prize_cols[:3]]
    
    # 열 이름 표준화
    df_clean.columns = ['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3']
    
    # 기존 CSV 로드
    try:
        existing = pd.read_csv('lotto_data.csv')
        print(f'✅ 기존 데이터: {len(existing)}개 회차')
    except FileNotFoundError:
        existing = pd.DataFrame()
        print('⚠️ 기존 CSV 없음, 새로 생성')
    
    # 병합
    combined = pd.concat([df_clean, existing]).drop_duplicates(subset=['round'], keep='first')
    combined = combined.sort_values('round', ascending=False)
    
    # 저장
    combined.to_csv('lotto_data.csv', index=False)
    print(f'✅ CSV 업데이트 완료: {len(combined)}개 회차')
    print(f'📊 추가된 회차: {", ".join(map(str, df_clean["round"].tolist()))}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('사용법: python update_lotto_csv.py <엑셀파일.xlsx>')
        sys.exit(1)
    
    update_lotto_csv(sys.argv[1])
```

**사용법**:
```bash
python update_lotto_csv.py lotto_download.xlsx
git add lotto_data.csv
git commit -m "Update lotto data"
git push
```

---

## 📅 업데이트 주기

- **매주 토요일 오후 9시 이후**: 새 추첨 결과 발표
- **매주 일요일**: CSV 업데이트 (5분 소요)

---

## 🔍 문제 해결

### CSV 파일이 인식되지 않음
- UTF-8 인코딩 확인
- 헤더 행 존재 여부 확인
- 쉼표 구분 확인

### 당첨금이 0으로 표시됨
- 엑셀 파일에서 당첨금 열 확인
- 숫자 형식인지 확인 (텍스트 아님)

### 날짜 형식 오류
- YYYY.MM.DD 형식 확인
- 예: 2024.11.02

---

## 💡 팁

1. **한 번에 여러 회차 업데이트**: 
   - 엑셀 다운로드 시 범위를 넓게 (예: 1180~1195)
   - CSV 파일이 자동으로 중복 제거

2. **GitHub Actions 자동화**:
   - 매주 일요일 자동으로 엑셀 다운로드 및 CSV 업데이트
   - 고급 사용자용 (설정 파일 필요)

3. **백업**:
   - 업데이트 전 `lotto_data.csv` 백업
   - Git 히스토리로 언제든 복구 가능

