import pyupbit
import os
from dotenv import load_dotenv
import json
from tabulate import tabulate

# .env 파일 로드
load_dotenv() 
access = os.getenv("ACCESS_KEY")
secret = os.getenv("SECRET_KEY")  

# Upbit 객체 생성
upbit = pyupbit.Upbit(access, secret)

print("\n\n=============== 내 정보 조회 ==============")

# KRW-BTC 조회
btc = upbit.get_balance("KRW-BTC")      
print(f"BTC 보유수량: {btc}")

# 보유 현금 조회
print(f"보유 현금: {upbit.get_balance('KRW')}")

# 전체 잔고 조회
# balances = upbit.get_balances()
# formatted = json.dumps(balances, indent=4, ensure_ascii=False)
# print(f"전체 잔고: {formatted}")

# 전체 잔고 조회2
balances = upbit.get_balances()
table = []
for b in balances:
    table.append([
        b["currency"],
        b["balance"],
        b["avg_buy_price"],
        b["unit_currency"],
        
    ])

print(tabulate(table, headers=["코인", "보유수량", "평단가", "기준통화"], tablefmt="pretty"))

