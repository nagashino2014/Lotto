#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로또 전체 데이터 다운로드 스크립트
1회차부터 최신 회차까지 모든 데이터를 CSV로 저장
"""

import requests
import csv
import time
import sys
from datetime import datetime

# Windows 콘솔 인코딩 설정
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

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
            else:
                return None
    except Exception as e:
        print(f"  ⚠️ 오류 발생: {e}")
        return None

def download_all_lotto_data(start_round=1, end_round=None):
    """전체 로또 데이터 다운로드"""
    
    if end_round is None:
        # 최신 회차 찾기
        print("최신 회차 확인 중...")
        for i in range(2000, 1000, -1):
            data = fetch_lotto_data(i)
            if data:
                end_round = i
                print(f"✅ 최신 회차: {end_round}회")
                break
            time.sleep(0.1)
    
    print(f"\n📥 {start_round}회 ~ {end_round}회 다운로드 시작...")
    print(f"예상 소요 시간: 약 {(end_round - start_round + 1) * 0.5 / 60:.1f}분\n")
    
    all_data = []
    failed_rounds = []
    
    for round_num in range(start_round, end_round + 1):
        print(f"  {round_num}/{end_round}회 조회 중...", end='\r')
        
        data = fetch_lotto_data(round_num)
        
        if data:
            all_data.append(data)
        else:
            failed_rounds.append(round_num)
        
        # API 과부하 방지
        time.sleep(0.5)
        
        # 100회마다 진행상황 저장
        if round_num % 100 == 0:
            print(f"\n  ✅ {round_num}회까지 완료 ({len(all_data)}개 수집)")
    
    print(f"\n\n✅ 다운로드 완료!")
    print(f"  - 성공: {len(all_data)}개 회차")
    if failed_rounds:
        print(f"  - 실패: {len(failed_rounds)}개 회차 {failed_rounds[:10]}...")
    
    return all_data

def save_to_csv(data, filename='lotto_data.csv'):
    """CSV 파일로 저장"""
    
    if not data:
        print("저장할 데이터가 없습니다.")
        return
    
    # 회차 내림차순 정렬 (최신이 위로)
    data.sort(key=lambda x: x['round'], reverse=True)
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
    
    print(f"\n💾 CSV 파일 저장 완료: {filename}")
    print(f"  - 총 {len(data)}개 회차")
    print(f"  - 최신: {data[0]['round']}회 ({data[0]['date']})")
    print(f"  - 최초: {data[-1]['round']}회 ({data[-1]['date']})")

if __name__ == '__main__':
    print("=" * 60)
    print("🎲 로또 전체 데이터 다운로드")
    print("=" * 60)
    
    # 1회차부터 최신까지 다운로드
    all_data = download_all_lotto_data(start_round=1)
    
    # CSV 저장
    save_to_csv(all_data)
    
    print("\n" + "=" * 60)
    print("✅ 완료!")
    print("=" * 60)

