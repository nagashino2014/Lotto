#!/usr/bin/env python3
"""
로또 데이터 자동 업데이트 스크립트
동행복권 API를 통해 최신 회차 데이터를 가져와 CSV에 추가합니다.
"""

import requests
import pandas as pd
import time
from datetime import datetime

def fetch_lotto_round(round_num):
    """특정 회차의 로또 데이터를 API에서 가져오기"""
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # 추첨 전 회차 체크
        if data.get('returnValue') == 'fail':
            return None
        
        # 데이터 추출
        return {
            'round': data['drwNo'],
            'date': data['drwNoDate'],
            'num1': data['drwtNo1'],
            'num2': data['drwtNo2'],
            'num3': data['drwtNo3'],
            'num4': data['drwtNo4'],
            'num5': data['drwtNo5'],
            'num6': data['drwtNo6'],
            'bonus': data['bnusNo'],
            'prize1': data.get('firstWinamnt', 0),
            'prize2': data.get('secondWinamnt', 0),
            'prize3': data.get('thirdWinamnt', 0)
        }
    except Exception as e:
        print(f"❌ {round_num}회차 조회 실패: {e}")
        return None

def load_existing_csv():
    """기존 CSV 파일 로드"""
    try:
        df = pd.read_csv('lotto_data.csv')
        print(f"✅ 기존 데이터 로드: {len(df)}개 회차")
        return df
    except FileNotFoundError:
        print("⚠️ 기존 CSV 파일 없음, 새로 생성")
        return pd.DataFrame(columns=['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3'])

def get_latest_round_number():
    """최신 회차 번호 찾기 (역순 탐색)"""
    # 대략적인 최신 회차 계산 (2002년 12월 7일 1회차 시작, 주 1회)
    from datetime import date
    start_date = date(2002, 12, 7)
    today = date.today()
    weeks_passed = (today - start_date).days // 7
    estimated_round = weeks_passed + 1
    
    # 역순으로 최대 10회차까지 확인
    for round_num in range(estimated_round + 5, estimated_round - 10, -1):
        data = fetch_lotto_round(round_num)
        if data:
            print(f"✅ 최신 회차 확인: {round_num}회")
            return round_num
        time.sleep(0.5)  # API 부하 방지
    
    return estimated_round

def update_lotto_data():
    """로또 데이터 업데이트"""
    print("=" * 60)
    print("🎰 로또 데이터 자동 업데이트 시작")
    print(f"⏰ 실행 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 기존 CSV 로드
    existing_df = load_existing_csv()
    
    # 기존 최대 회차
    if len(existing_df) > 0:
        max_existing_round = existing_df['round'].max()
        print(f"📊 현재 최대 회차: {max_existing_round}회")
    else:
        max_existing_round = 0
        print("📊 신규 데이터베이스 생성")
    
    # 최신 회차 확인
    latest_round = get_latest_round_number()
    
    if latest_round <= max_existing_round:
        print(f"✅ 이미 최신 상태입니다 (최대 {max_existing_round}회)")
        return
    
    # 누락된 회차 추가
    new_data = []
    for round_num in range(max_existing_round + 1, latest_round + 1):
        print(f"📥 {round_num}회차 데이터 가져오는 중...")
        data = fetch_lotto_round(round_num)
        
        if data:
            new_data.append(data)
            print(f"   ✅ 번호: {data['num1']}, {data['num2']}, {data['num3']}, {data['num4']}, {data['num5']}, {data['num6']} + {data['bonus']}")
        else:
            print(f"   ⚠️ {round_num}회차 데이터 없음 (아직 추첨 전일 수 있음)")
            break
        
        time.sleep(1)  # API 부하 방지
    
    if new_data:
        # 새 데이터를 DataFrame으로 변환
        new_df = pd.DataFrame(new_data)
        
        # 기존 데이터와 병합
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # 회차 기준 정렬 (내림차순)
        combined_df = combined_df.sort_values('round', ascending=False)
        
        # 중복 제거
        combined_df = combined_df.drop_duplicates(subset=['round'], keep='first')
        
        # CSV 저장
        combined_df.to_csv('lotto_data.csv', index=False)
        
        print("=" * 60)
        print(f"✅ 업데이트 완료!")
        print(f"📊 추가된 회차: {len(new_data)}개")
        print(f"📊 총 회차: {len(combined_df)}개")
        print(f"📊 최신 회차: {combined_df['round'].max()}회")
        print("=" * 60)
    else:
        print("=" * 60)
        print("ℹ️ 추가할 새 데이터가 없습니다")
        print("=" * 60)

if __name__ == '__main__':
    try:
        update_lotto_data()
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

