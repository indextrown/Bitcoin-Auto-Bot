# import pyupbit
# from dotenv import load_dotenv
# import os
# import pandas as pd
# import requests
# from datetime import datetime

# # load .env
# load_dotenv()

# # key
# Access_Key = os.environ.get('Access_Key')
# Secret_Key = os.environ.get('Secret_Key')
# Slack_key = os.environ.get("Slack_Key")
# upbit = pyupbit.Upbit(Access_Key, Secret_Key)

# def alarm(token, channel, text):
#     requests.post("https://slack.com/api/chat.postMessage",
#         headers={"Authorization": "Bearer "+token},
#         data={"channel": channel,"text": text})

# #RSI지표 수치를 구해준다. 첫번째: 분봉/일봉 정보, 두번째: 기간
# # 지정한 기간 동안의 전일 대비 상승분의 평균 / (전일대비 상승분의 평균+하락분의 평균)
# def GetRSI(ohlcv,period):
#     ohlcv["close"] = ohlcv["close"]
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# def coinbot():
#     #비트코인의 240분봉 정보를 가져온다.  
#     df = pyupbit.get_ohlcv("KRW-BTC",interval="minute240")

#     # RSI14 계산
#     rsi14_series = GetRSI(df, 14)
#     current_rsi14 = float(rsi14_series.iloc[-1])  # 현재 RSI 값
#     previous_rsi14 = float(rsi14_series.iloc[-2])  # 이전 4시간 봉의 RSI 값

#     # print("BTC_BOT_WORKING")
#     # print("NOW RSI:", current_rsi14)

#     # 알림 메시지 작성
#     current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     message = f"""
#     [비트코인 매수!]
#     - 현재 시간: {current_time}
#     - 현재 RSI(실시간): {current_rsi14:.2f}
#     - 이전 4시간 봉 RSI(고정값): {previous_rsi14:.2f}
#     """

#     # 4시간분봉 기준으로 rs4지표가 30이하면 매수진행
#     if current_rsi14 <= 30: 
#         # 비트코인 시장가 구매
#         buy_result = upbit.buy_market_order("KRW-BTC", 5000)
#         message += f"""
#         - 매수 진행: RSI 값이 30 이하
#         - 매수 금액: 5,000원
#         - 주문 결과: {buy_result}
#         """
#         print(message)
#         # 슬랙 알림 발송
#         alarm(Slack_key, "#aws-ec2-alarm", message)
#     else:
#         message += "- 매수 조건 미충족: RSI 값이 30 초과\n"
#         # alarm(Slack_key, "#aws-ec2-alarm", message)
#         print(message)


# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime

# plt.rc('font', family='AppleGothic')        # Mac: 
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(start_date="2024-01-01", end_date="2024-12-31"):
#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= start_date) & (historical_data.index <= end_date)]
    
#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
        
#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     plt.figure(figsize=(14, 7))
#     plt.plot(timestamps, total_asset_values, label="총 자산 가치")
#     plt.title("2024년 백테스팅 결과")
#     plt.xlabel("날짜")
#     plt.ylabel("총 자산 가치 (KRW)")
#     plt.legend()
#     plt.grid(True)
#     plt.show()


# # 백테스팅 실행
# backtest_coinbot()


# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime

# plt.rc('font', family='AppleGothic')        # Mac
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(start_date="2024-01-01", end_date="2024-12-31"):
#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= start_date) & (historical_data.index <= end_date)]

#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록
#     buy_points = []  # 매수 시점 기록
#     sell_points = []  # 매도 시점 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]

#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy
#                 buy_points.append((historical_data.index[i], cash + btc_balance * historical_data.iloc[i]['close']))

#         # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
#         if rsi >= 70 and btc_balance > 0:
#             cash += btc_balance * historical_data.iloc[i]['close']
#             sell_points.append((historical_data.index[i], cash))
#             btc_balance = 0

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     plt.figure(figsize=(14, 7))
#     plt.plot(timestamps, total_asset_values, label="총 자산 가치")

#     # 매수/매도 시점 표시
#     if buy_points:
#         buy_x, buy_y = zip(*buy_points)
#         plt.scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
#     if sell_points:
#         sell_x, sell_y = zip(*sell_points)
#         plt.scatter(sell_x, sell_y, color="red", label="매도", marker="o")

#     plt.title("2024년 백테스팅 결과")
#     plt.xlabel("날짜")
#     plt.ylabel("총 자산 가치 (KRW)")
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# # 백테스팅 실행
# backtest_coinbot()




# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime

# plt.rc('font', family='AppleGothic')        # Mac
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(start_date="2024-01-01", end_date="2024-12-31"):
#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= start_date) & (historical_data.index <= end_date)]

#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록
#     buy_points = []  # 매수 시점 기록
#     sell_points = []  # 매도 시점 기록
#     rsi_values = []  # RSI 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
#         rsi_values.append(rsi)

#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy
#                 buy_points.append((historical_data.index[i], rsi))

#         # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
#         if rsi >= 70 and btc_balance > 0:
#             cash += btc_balance * historical_data.iloc[i]['close']
#             sell_points.append((historical_data.index[i], rsi))
#             btc_balance = 0

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     fig, axs = plt.subplots(2, 1, figsize=(10, 8))

#     # 총 자산 가치 그래프
#     axs[0].plot(timestamps, total_asset_values, label="총 자산 가치")
#     axs[0].set_title("총 자산 가치")
#     axs[0].set_xlabel("날짜")
#     axs[0].set_ylabel("총 자산 가치 (KRW)")
#     axs[0].legend()
#     axs[0].grid(True)

#     # RSI 그래프
#     axs[1].plot(timestamps, rsi_values, label="RSI", color="green")
#     axs[1].set_title("RSI 지표 및 매수/매도 포인트")
#     axs[1].set_xlabel("날짜")
#     axs[1].set_ylabel("RSI 값")
#     axs[1].axhline(30, color="blue", linestyle="--", label="매수 기준 (30)")
#     axs[1].axhline(70, color="red", linestyle="--", label="매도 기준 (70)")

#     # 매수/매도 포인트 표시
#     if buy_points:
#         buy_x, buy_y = zip(*buy_points)
#         axs[1].scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
#     if sell_points:
#         sell_x, sell_y = zip(*sell_points)
#         axs[1].scatter(sell_x, sell_y, color="red", label="매도", marker="o")

#     axs[1].legend()
#     axs[1].grid(True)

#     plt.tight_layout()
#     plt.show()

# # 백테스팅 실행
# backtest_coinbot()


# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime

# plt.rc('font', family='AppleGothic')        # Mac
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(start_date="2024-01-01", end_date="2024-12-31"):
#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= start_date) & (historical_data.index <= end_date)]

#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록
#     buy_points = []  # 매수 시점 기록
#     sell_points = []  # 매도 시점 기록
#     rsi_values = []  # RSI 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
#         rsi_values.append(rsi)

#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy
#                 buy_points.append((historical_data.index[i], rsi))

#         # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
#         if rsi >= 70 and btc_balance > 0:
#             cash += btc_balance * historical_data.iloc[i]['close']
#             sell_points.append((historical_data.index[i], rsi))
#             btc_balance = 0

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

#     # 총 자산 가치 그래프
#     axs[0].plot(timestamps, total_asset_values, label="총 자산 가치")
#     axs[0].set_title("총 자산 가치")
#     axs[0].set_ylabel("총 자산 가치 (KRW)")
#     axs[0].legend()
#     axs[0].grid(True)

#     # RSI 그래프
#     axs[1].plot(timestamps, rsi_values, label="RSI", color="green")
#     axs[1].set_title("RSI 지표 및 매수/매도 포인트")
#     axs[1].set_xlabel("날짜")
#     axs[1].set_ylabel("RSI 값")
#     axs[1].axhline(30, color="blue", linestyle="--", label="매수 기준 (30)")
#     axs[1].axhline(70, color="red", linestyle="--", label="매도 기준 (70)")

#     # 매수/매도 포인트 표시
#     if buy_points:
#         buy_x, buy_y = zip(*buy_points)
#         axs[1].scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
#     if sell_points:
#         sell_x, sell_y = zip(*sell_points)
#         axs[1].scatter(sell_x, sell_y, color="red", label="매도", marker="o")

#     axs[1].legend()
#     axs[1].grid(True)

#     plt.tight_layout()
#     plt.show()

# # 백테스팅 실행
# backtest_coinbot()


# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime, timedelta

# plt.rc('font', family='AppleGothic')        # Mac
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(period="year"):
#     # 기간 설정
#     end_date = datetime.now()
#     if period == "day":
#         start_date = end_date - timedelta(days=1)
#     elif period == "week":
#         start_date = end_date - timedelta(weeks=1)
#     elif period == "month":
#         start_date = end_date - timedelta(days=30)
#     elif period == "year":
#         start_date = end_date - timedelta(days=365)
#     else:
#         raise ValueError("Invalid period. Choose from 'day', 'week', 'month', or 'year'.")

#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= str(start_date)) & (historical_data.index <= str(end_date))]

#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록
#     buy_points = []  # 매수 시점 기록
#     sell_points = []  # 매도 시점 기록
#     rsi_values = []  # RSI 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
#         rsi_values.append(rsi)

#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy
#                 buy_points.append((historical_data.index[i], rsi))

#         # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
#         if rsi >= 70 and btc_balance > 0:
#             cash += btc_balance * historical_data.iloc[i]['close']
#             sell_points.append((historical_data.index[i], rsi))
#             btc_balance = 0

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

#     # 총 자산 가치 그래프
#     axs[0].plot(timestamps, total_asset_values, label="총 자산 가치")
#     axs[0].set_title("총 자산 가치")
#     axs[0].set_ylabel("총 자산 가치 (KRW)")
#     axs[0].legend()
#     axs[0].grid(True)

#     # RSI 그래프
#     axs[1].plot(timestamps, rsi_values, label="RSI", color="green")
#     axs[1].set_title("RSI 지표 및 매수/매도 포인트")
#     axs[1].set_xlabel("날짜")
#     axs[1].set_ylabel("RSI 값")
#     axs[1].axhline(30, color="blue", linestyle="--", label="매수 기준 (30)")
#     axs[1].axhline(70, color="red", linestyle="--", label="매도 기준 (70)")

#     # 매수/매도 포인트 표시
#     if buy_points:
#         buy_x, buy_y = zip(*buy_points)
#         axs[1].scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
#     if sell_points:
#         sell_x, sell_y = zip(*sell_points)
#         axs[1].scatter(sell_x, sell_y, color="red", label="매도", marker="o")

#     axs[1].legend()
#     axs[1].grid(True)

#     plt.tight_layout()
#     plt.show()

# # 백테스팅 실행: 원하는 기간 선택 ("day", "week", "month", "year")
# backtest_coinbot(period="month")



# import matplotlib.pyplot as plt
# import pyupbit
# import pandas as pd
# from datetime import datetime, timedelta

# plt.rc('font', family='AppleGothic')        # Mac
# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# # RSI 계산 함수
# def GetRSI(ohlcv, period):
#     delta = ohlcv["close"].diff()
#     up, down = delta.copy(), delta.copy()
#     up[up < 0] = 0
#     down[down > 0] = 0
#     _gain = up.ewm(com=(period - 1), min_periods=period).mean()
#     _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
#     RS = _gain / _loss
#     return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# # 백테스팅 함수
# def backtest_coinbot(period="year", start_date=None, end_date=None):
#     # 기간 설정
#     if start_date and end_date:
#         start_date = datetime.strptime(start_date, "%Y-%m-%d")
#         end_date = datetime.strptime(end_date, "%Y-%m-%d")
#     else:
#         end_date = datetime.now()
#         if period == "day":
#             start_date = end_date - timedelta(days=1)
#         elif period == "week":
#             start_date = end_date - timedelta(weeks=1)
#         elif period == "month":
#             start_date = end_date - timedelta(days=30)
#         elif period == "year":
#             start_date = end_date - timedelta(days=365)
#         else:
#             raise ValueError("Invalid period. Choose from 'day', 'week', 'month', 'year', or provide 'start_date' and 'end_date'.")

#     # 4시간봉 데이터 가져오기
#     historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
#     historical_data = historical_data[(historical_data.index >= str(start_date)) & (historical_data.index <= str(end_date))]

#     # 초기 자산 설정
#     cash = 1000000  # 초기 현금 (KRW)
#     btc_balance = 0  # 초기 비트코인 보유량
#     total_asset_values = []  # 총 자산 기록
#     timestamps = []  # 타임스탬프 기록
#     buy_points = []  # 매수 시점 기록
#     sell_points = []  # 매도 시점 기록
#     rsi_values = []  # RSI 기록

#     for i in range(len(historical_data)):
#         # RSI 계산
#         simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
#         rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
#         rsi_values.append(rsi)

#         # 매수 조건 시뮬레이션
#         if rsi <= 30:
#             btc_to_buy = 5000 / historical_data.iloc[i]['close']
#             if cash >= 5000:
#                 cash -= 5000
#                 btc_balance += btc_to_buy
#                 buy_points.append((historical_data.index[i], rsi))

#         # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
#         if rsi >= 70 and btc_balance > 0:
#             cash += btc_balance * historical_data.iloc[i]['close']
#             sell_points.append((historical_data.index[i], rsi))
#             btc_balance = 0

#         # 총 자산 계산
#         total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
#         total_asset_values.append(total_asset_value)
#         timestamps.append(historical_data.index[i])  # 타임스탬프 추가

#     # 그래프 시각화
#     fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

#     # 총 자산 가치 그래프
#     axs[0].plot(timestamps, total_asset_values, label="총 자산 가치")
#     axs[0].set_title("총 자산 가치")
#     axs[0].set_ylabel("총 자산 가치 (KRW)")
#     axs[0].legend()
#     axs[0].grid(True)

#     # RSI 그래프
#     axs[1].plot(timestamps, rsi_values, label="RSI", color="green")
#     axs[1].set_title("RSI 지표 및 매수/매도 포인트")
#     axs[1].set_xlabel("날짜")
#     axs[1].set_ylabel("RSI 값")
#     axs[1].axhline(30, color="blue", linestyle="--", label="매수 기준 (30)")
#     axs[1].axhline(70, color="red", linestyle="--", label="매도 기준 (70)")

#     # 매수/매도 포인트 표시
#     if buy_points:
#         buy_x, buy_y = zip(*buy_points)
#         axs[1].scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
#     if sell_points:
#         sell_x, sell_y = zip(*sell_points)
#         axs[1].scatter(sell_x, sell_y, color="red", label="매도", marker="o")

#     axs[1].legend()
#     axs[1].grid(True)

#     plt.tight_layout()
#     plt.show()

# # 백테스팅 실행: 원하는 기간 선택 ("day", "week", "month", "year") 또는 특정 날짜 지정
# backtest_coinbot(period="year")


import matplotlib.pyplot as plt
import pyupbit
import pandas as pd
from datetime import datetime, timedelta

plt.rc('font', family='AppleGothic')        # Mac
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# RSI 계산 함수
def GetRSI(ohlcv, period):
    delta = ohlcv["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

# 백테스팅 함수
def backtest_coinbot(period="year", start_date=None, end_date=None):
    # 기간 설정
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end_date = datetime.now()
        if period == "day":
            start_date = end_date - timedelta(days=1)
        elif period == "week":
            start_date = end_date - timedelta(weeks=1)
        elif period == "month":
            start_date = end_date - timedelta(days=30)
        elif period == "year":
            start_date = end_date - timedelta(days=365)
        else:
            raise ValueError("Invalid period. Choose from 'day', 'week', 'month', 'year', or provide 'start_date' and 'end_date'.")

    # 4시간봉 데이터 가져오기
    historical_data = pyupbit.get_ohlcv("KRW-BTC", interval="minute240", count=2000)
    historical_data = historical_data[(historical_data.index >= str(start_date)) & (historical_data.index <= str(end_date))]

    # 초기 자산 설정
    cash = 1000000  # 초기 현금 (KRW)
    btc_balance = 0  # 초기 비트코인 보유량
    total_asset_values = []  # 총 자산 기록
    timestamps = []  # 타임스탬프 기록
    buy_points = []  # 매수 시점 기록
    sell_points = []  # 매도 시점 기록
    rsi_values = []  # RSI 기록

    for i in range(len(historical_data)):
        # RSI 계산
        simulated_ohlcv = historical_data.iloc[:i + 1]  # iloc으로 정수 인덱스 슬라이싱
        rsi = GetRSI(simulated_ohlcv, 14).iloc[-1]
        rsi_values.append(rsi)

        # 매수 조건 시뮬레이션
        if rsi <= 30:
            btc_to_buy = 5000 / historical_data.iloc[i]['close']
            if cash >= 5000:
                cash -= 5000
                btc_balance += btc_to_buy
                buy_points.append((historical_data.index[i], rsi))

        # 매도 조건 시뮬레이션 (예: RSI >= 70일 때 매도)
        if rsi >= 70 and btc_balance > 0:
            cash += btc_balance * historical_data.iloc[i]['close']
            sell_points.append((historical_data.index[i], rsi))
            btc_balance = 0

        # 총 자산 계산
        total_asset_value = cash + (btc_balance * historical_data.iloc[i]['close'])
        total_asset_values.append(total_asset_value)
        timestamps.append(historical_data.index[i])  # 타임스탬프 추가

    # 그래프 시각화
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # 총 자산 가치 그래프
    axs[0].plot(timestamps, total_asset_values, label="총 자산 가치")
    axs[0].set_title("총 자산 가치")
    axs[0].set_ylabel("총 자산 가치 (KRW)")
    axs[0].legend()
    axs[0].grid(True)

    # RSI 그래프
    axs[1].plot(timestamps, rsi_values, label="RSI", color="green")
    axs[1].set_title("RSI 지표 및 매수/매도 포인트")
    axs[1].set_xlabel("날짜")
    axs[1].set_ylabel("RSI 값")
    axs[1].axhline(30, color="blue", linestyle="--", label="매수 기준 (30)")
    axs[1].axhline(70, color="red", linestyle="--", label="매도 기준 (70)")

    # 매수/매도 포인트 표시
    if buy_points:
        buy_x, buy_y = zip(*buy_points)
        axs[1].scatter(buy_x, buy_y, color="blue", label="매수", marker="o")
    if sell_points:
        sell_x, sell_y = zip(*sell_points)
        axs[1].scatter(sell_x, sell_y, color="red", label="매도", marker="o")

    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

# 백테스팅 실행: 원하는 기간 선택 ("day", "week", "month", "year") 또는 특정 날짜 지정
backtest_coinbot(start_date="2024-12-01", end_date="2025-01-31")
