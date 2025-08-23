# RSI지표가 30 이하일때 30분마다 구매하는 로직

# 240분봉 기준이라 4시간마다 바뀌는 rsi지표가 30이하면 매수 진행하겠다
# 4~8사이에 rsi지표가 30이하라면(실시간으로보면 30이하가 아닐수도)
# 서버에 30분마다 실행하도록 설정한다면 총 8번 실행될텐데 30이하라면 매수 진행(실시간으로 변하는 값)
# 만약 실시간으로 변하는 값말고 이전 고정값을 보고싶다면 -2인덱싱을해서 0~4시를 보면됨
# * /30 * * * * python3 /var/bitcoin/upbit_auto_btc.py

"""
1. 4시간 봉 기준 RSI 지표
240분봉은 4시간 간격으로 집계된 데이터(시가, 고가, 저가, 종가)를 기준으로 RSI를 계산합니다.
예: 0시, 4시, 8시, 12시...마다 새로 값이 갱신됩니다.
RSI는 각 4시간 봉 데이터의 **종가(close)**를 기준으로 계산되므로, RSI 값은 4시간마다 고정됩니다.


2. 실시간으로 확인할 때와 고정 값을 볼 때의 차이
실시간 값
코드는 30분마다 실행되며, pyupbit.get_ohlcv()로 최신 4시간 봉 데이터를 가져옵니다.
예를 들어, 4~8시 구간에서 30분마다 실행되면, 이 값은 4시간 동안 변하는 최신 데이터를 기준으로 RSI를 계산합니다.
즉, 8시 이전에는 최종적으로 확정된 값이 아니므로, RSI 값이 변동될 수 있습니다.
고정 값
4시간 구간이 끝난 이후(예: 0~4시 구간이 끝난 4시), 해당 구간의 데이터는 고정됩니다.
이 고정된 데이터를 보려면 iloc[-2]와 같은 방식으로 이전 봉 데이터를 선택합니다.
-1: 현재 가장 최신 데이터 (실시간 변동 가능)
-2: 고정된 이전 4시간 봉 데이터 (예: 0~4시 데이터)

3. 30분마다 실행되는 경우의 동작
크론탭을 통해 30분마다 코드가 실행됩니다. 예를 들어:
4시: 0~4시 구간의 RSI 값이 고정됨.
4시 30분: 4~8시 구간의 값이 변동하며 실시간 RSI를 계산.
5시: 여전히 4~8시 구간의 값이 변동하며 실시간 RSI 계산.
...
8시: 4~8시 구간의 값이 고정됨.
이렇게 하면 4~8시 동안 총 8번 실행되며, 매 실행 시점에서 RSI 값이 다를 수 있습니다. 따라서:
실시간 RSI는 구간 내에서 계속 변할 수 있습니다.
고정된 RSI를 보려면 이전 구간(예: 0~4시)의 데이터를 사용해야 합니다.


실제 상황에서의 차이
실시간 값으로 실행
4~8시 구간 동안 RSI가 30 이하로 내려갔다가 다시 올라갈 수 있음.
이 경우, 실시간 값으로 판단하면 매수할 수도, 안 할 수도 있습니다.
고정 값으로 실행
0~4시 구간의 고정된 RSI 값이 30 이하라면, 4시 이후 매수를 진행합니다.
실행 시점마다 변동 없이 고정된 기준으로 매수 여부를 판단합니다.

"""

import pyupbit
from dotenv import load_dotenv
import os
import pandas as pd
import requests
from datetime import datetime, timedelta

# load .env
load_dotenv()

# key
Access_Key = os.environ.get('Access_Key')
Secret_Key = os.environ.get('Secret_Key')
Slack_key = os.environ.get("Slack_Key")
upbit = pyupbit.Upbit(Access_Key, Secret_Key)

def alarm(token, channel, text):
    requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text})

#RSI지표 수치를 구해준다. 첫번째: 분봉/일봉 정보, 두번째: 기간
# 지정한 기간 동안의 전일 대비 상승분의 평균 / (전일대비 상승분의 평균+하락분의 평균)
def GetRSI(ohlcv,period):
    ohlcv["close"] = ohlcv["close"]
    delta = ohlcv["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

#비트코인의 240분봉 정보를 가져온다.  
df = pyupbit.get_ohlcv("KRW-BTC",interval="minute240")

# RSI14 계산
rsi14_series = GetRSI(df, 14)
current_rsi14 = float(rsi14_series.iloc[-1])  # 현재 RSI 값
previous_rsi14 = float(rsi14_series.iloc[-2])  # 이전 4시간 봉의 RSI 값

# ohlcv 데이터에서 4시간봉 시작 및 종료 시간 파악
last_candle_time = df.index[-1]  # 가장 최근 봉의 시작 시간
start_time_str = last_candle_time.strftime('%Y-%m-%d %H:%M:%S')
end_time = last_candle_time + timedelta(hours=4)
end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')


# print("BTC_BOT_WORKING")
# print("NOW RSI:", current_rsi14)

# 알림 메시지 작성
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 4시간분봉 기준으로 rs4지표가 30이하면 매수진행
if current_rsi14 <= 30: 
    # 비트코인 시장가 구매
    buy_result = upbit.buy_market_order("KRW-BTC", 5000)
    message = f"""
[!!비트코인 매수 성공!!]
- 현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 현재 4시간봉 구간: {start_time_str} ~ {end_time_str}
- 현재 RSI(실시간): {current_rsi14:.2f}
- 이전 4시간 봉 RSI(고정값): {previous_rsi14:.2f}
- 매수 진행: RSI 값이 30 이하
- 매수 금액: 5,000원
- 주문 결과: {buy_result}\n
"""
    print(message)
    # 슬랙 알림 발송
    alarm(Slack_key, "#aws-ec2-alarm", message)

else:
    message = f"""
[매수 실패]
- 현재 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 현재 4시간봉 구간: {start_time_str} ~ {end_time_str}
- 현재 RSI(실시간): {current_rsi14:.2f}
- 이전 4시간 봉 RSI(고정값): {previous_rsi14:.2f}
- 매수 조건 미충족: RSI 값이 30 초과\n
"""
    # alarm(Slack_key, "#aws-ec2-alarm", message)
    print(message)

