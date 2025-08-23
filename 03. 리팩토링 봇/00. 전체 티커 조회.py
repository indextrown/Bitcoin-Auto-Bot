# https://github.com/sharebook-kr/pyupbit

import pyupbit

# fiat: KRW/BTC/USDT
print(pyupbit.get_tickers()) # 전체 티커 조회
# print(pyupbit.get_tickers("KRW")) # KRW 기준 티커 조회
# print(pyupbit.get_tickers("BTC")) # BTC 기준 티커 조회