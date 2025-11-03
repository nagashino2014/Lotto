#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
로또 빠른 다운로드 (동시 요청)
"""

import requests
import csv
import concurrent.futures
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def fetch_lotto_data(round_num):
    """특정 회차 데이터 가져오기"""
    url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
    
    try:
        response = requests.get(url, timeout=5)
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
    except:
        pass
    return None

def download_batch(start, end, max_workers=10):
    """배치로 다운로드"""
    print(f"Downloading rounds {start}-{end}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_lotto_data, r): r for r in range(start, end + 1)}
        results = []
        
        for future in concurrent.futures.as_completed(futures):
            round_num = futures[future]
            try:
                data = future.result()
                if data:
                    results.append(data)
                    if len(results) % 50 == 0:
                        print(f"  Progress: {len(results)}/{end-start+1}")
            except Exception as e:
                print(f"  Error at round {round_num}: {e}")
        
        return results

def main():
    print("="*60)
    print("Fast Lotto Data Download (1-1196)")
    print("="*60)
    
    all_data = []
    
    # 배치로 나누어 다운로드 (100회씩)
    for start in range(1, 1197, 100):
        end = min(start + 99, 1196)
        batch_data = download_batch(start, end)
        all_data.extend(batch_data)
        print(f"  Batch {start}-{end}: {len(batch_data)} rounds collected\n")
    
    # 회차 내림차순 정렬
    all_data.sort(key=lambda x: x['round'], reverse=True)
    
    # CSV 저장
    print(f"\nSaving {len(all_data)} rounds to lotto_data.csv...")
    with open('lotto_data.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['round', 'date', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'bonus', 'prize1', 'prize2', 'prize3']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"\nDone! {len(all_data)} rounds saved.")
    print(f"Latest: Round {all_data[0]['round']} ({all_data[0]['date']})")
    print(f"Oldest: Round {all_data[-1]['round']} ({all_data[-1]['date']})")

if __name__ == '__main__':
    main()

