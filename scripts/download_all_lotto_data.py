#!/usr/bin/env python3
"""
로또 전체 데이터 초기 다운로드 (1회 ~ 최신회차)
최초 1회만 실행하여 전체 데이터 생성
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
        
        if data.get('returnValue') == 'fail':
            return None
        
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
        print(f"[ERROR] {round_num}회차 실패: {e}")
        return None

def download_all_rounds(start_round=1, end_round=1196):
    """모든 회차 데이터 다운로드"""
    print("=" * 70)
    print("[LOTTO] 전체 데이터 다운로드 시작")
    print(f"[INFO] 범위: {start_round}회 ~ {end_round}회")
    print(f"[TIME] 시작 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    all_data = []
    failed_rounds = []
    
    for round_num in range(start_round, end_round + 1):
        # 진행 상황 표시
        if round_num % 10 == 0:
            print(f"\n[PROGRESS] 진행 중: {round_num}/{end_round} ({round_num/end_round*100:.1f}%)")
        
        # 데이터 가져오기
        data = fetch_lotto_round(round_num)
        
        if data:
            all_data.append(data)
            if round_num % 10 == 0:
                print(f"   [OK] {round_num}회: {data['num1']}, {data['num2']}, {data['num3']}, {data['num4']}, {data['num5']}, {data['num6']} + {data['bonus']}")
        else:
            failed_rounds.append(round_num)
            if round_num % 10 == 0:
                print(f"   [SKIP] {round_num}회: 데이터 없음")
        
        # API 부하 방지 (10회마다 1초 대기)
        if round_num % 10 == 0:
            time.sleep(1)
        else:
            time.sleep(0.1)
    
    # DataFrame 생성
    df = pd.DataFrame(all_data)
    
    # 회차 기준 내림차순 정렬
    df = df.sort_values('round', ascending=False)
    
    # CSV 저장
    df.to_csv('lotto_data.csv', index=False, encoding='utf-8')
    
    print("\n" + "=" * 70)
    print("[DONE] 다운로드 완료!")
    print(f"[OK] 성공: {len(all_data)}개 회차")
    print(f"[FAIL] 실패: {len(failed_rounds)}개 회차")
    if failed_rounds:
        print(f"   실패한 회차: {failed_rounds[:10]}{'...' if len(failed_rounds) > 10 else ''}")
    print(f"[FILE] 저장 위치: lotto_data.csv")
    print(f"[TIME] 완료 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # 샘플 데이터 출력
    print("\n[SAMPLE] 최근 5개 회차:")
    print(df.head(5).to_string(index=False))

if __name__ == '__main__':
    try:
        # 1회부터 1196회까지 다운로드
        download_all_rounds(1, 1196)
        print("\n[DONE] 완료! 이제 'git add lotto_data.csv && git commit && git push' 실행하세요.")
    except Exception as e:
        print(f"\n[ERROR] 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

