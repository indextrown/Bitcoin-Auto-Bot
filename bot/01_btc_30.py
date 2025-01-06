import pyupbit
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# key
Access_Key = os.environ.get('Access_Key')
Secret_Key = os.environ.get('Secret_Key')
upbit = pyupbit.Upbit(Access_Key, Secret_Key)

# 비트코인 시장가 구매
upbit.buy_market_order("KRW-BTC", 5000)