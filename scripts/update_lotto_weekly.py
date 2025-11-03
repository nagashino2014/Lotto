#!/usr/bin/env python3
"""
로또 주간 업데이트 스크립트
GitHub Actions에서 매주 실행되어 최신 데이터를 추가
"""

import requests
import csv
import time
from datetime import datetime

def fetch_lotto_data(round_num):
    """특정 회차의 로또 데이터 가져오기"""
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data.get('returnValue') == 'success':
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
        return None
    except Exception as e:
        print(f"오류: {e}")
        return None

def get_latest_round_from_csv(filename='lotto_data.csv'):
    """CSV 파일에서 최신 회차 번호 가져오기"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            first_row = next(reader)
            return int(first_row['round'])
    except Exception:
        return 0

def find_latest_available_round():
    """API에서 사용 가능한 최신 회차 찾기"""
    print("최신 회차 확인 중...")
    
    # 현재 예상 회차부터 역순으로 검색
    for round_num in range(1300, 1100, -1):
        data = fetch_lotto_data(round_num)
        if data:
            print(f"✅ 최신 회차: {round_num}회")
            return round_num
        time.sleep(0.1)
    
    return None

def update_lotto_data():
    """기존 CSV에 최신 데이터 추가"""
    
    csv_latest = get_latest_round_from_csv()
    api_latest = find_latest_available_round()
    
    if not api_latest:
        print("❌ 최신 회차를 찾을 수 없습니다.")
        return False
    
    print(f"\nCSV 최신 회차: {csv_latest}회")
    print(f"API 최신 회차: {api_latest}회")
    
    if csv_latest >= api_latest:
        print(f"\n✅ 이미 최신 데이터입니다. (업데이트 불필요)")
        return False
    
    # 누락된 회차 다운로드
    print(f"\n📥 {csv_latest + 1}회 ~ {api_latest}회 다운로드 중...")
    new_data = []
    
    for round_num in range(csv_latest + 1, api_latest + 1):
        print(f"  {round_num}회 조회 중...")
        data = fetch_lotto_data(round_num)
        
        if data:
            new_data.append(data)
            print(f"    ✅ {round_num}회: {data['num1']}, {data['num2']}, {data['num3']}, {data['num4']}, {data['num5']}, {data['num6']} + {data['bonus']}")
        else:
            print(f"    ⚠️ {round_num}회 데이터 없음")
        
        time.sleep(0.5)
    
    if not new_data:
        print("\n⚠️ 새로운 데이터가 없습니다.")
        return False
    
    # 기존 CSV 읽기
    existing_data = []
    try:
        with open('lotto_data.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    except Exception as e:
        print(f"기존 데이터 읽기 실패: {e}")
    
    # 새 데이터 추가 (최신이 위로)
    all_data = new_data + existing_data
    
    # CSV 저장
    with open('lotto_data.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"\n✅ CSV 업데이트 완료!")
    print(f"  - 추가된 회차: {len(new_data)}개")
    print(f"  - 최신: {new_data[0]['round']}회 ({new_data[0]['date']})")
    print(f"  - 총 데이터: {len(all_data)}개 회차")
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("🎲 로또 주간 업데이트")
    print(f"⏰ 실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    updated = update_lotto_data()
    
    print("\n" + "=" * 60)
    if updated:
        print("✅ 업데이트 완료!")
    else:
        print("ℹ️ 업데이트 없음")
    print("=" * 60)

