# [made by index]
# rsi60분봉 기준으로 30이하일 때 분할매수 진행
# (15분마다 크론탭) == 4번의 매수 기회 생김
# (10분마다 크론탭) == 6번의 매수 기회 생김
# (5분마다 크론탭) == 12번의 매수 기회 생김

# (15분마다 크론탭) == 4번의 매수 기회 생김 -> 이걸로 진행예정
# 현재 실시간 값을 반영하기 때문에 4번 의 매수기회가 있어도 4번 다 확정으로 매수되는건 아님

import time
import pandas as pd
import pyupbit
from dotenv import load_dotenv
import os
import pandas as pd
#챕터7까지 진행하시면서 봇은 점차 완성이 되어 갑니다!!!
#챕터5까지 완강 후 봇을 돌리셔도 되지만 이왕이면 7까지 완강하신 후 돌리시는 걸 추천드려요!

# load .env
load_dotenv()

# key
Access_Key = os.environ.get('Access_Key')
Secret_Key = os.environ.get('Secret_Key')

#업비트 객체를 만들어요 액세스 키와 시크릿 키를 넣어서요.
upbit = pyupbit.Upbit(Access_Key, Secret_Key)

#아래 함수안의 내용은 참고로만 보세요! 제가 말씀드렸죠? 검증된 함수니 안의 내용 몰라도 그냥 가져다 쓰기만 하면 끝!
#RSI지표 수치를 구해준다. 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def GetRSI(ohlcv,period,st):
    #이 안의 내용이 어려우시죠? 넘어가셔도 되요. 우리는 이 함수가 RSI지표를 정확히 구해준다는 것만 알면 됩니다.
    ohlcv["close"] = ohlcv["close"]
    delta = ohlcv["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return float(pd.Series(100 - (100 / (1 + RS)), name="RSI").iloc[st])

#거래대금이 많은 순으로 코인 리스트를 얻는다. 첫번째 : Interval기간(day,week,minute15 ....), 두번째 : 몇개까지 
def GetTopCoinList(interval,top):
    print("--------------GetTopCoinList Start-------------------")

    #원화 마켓의 코인 티커를 리스트로 담아요.
    Tickers = pyupbit.get_tickers("KRW")

        #딕셔너리를 하나 만듭니다.
    dic_coin_money = dict()

    #for문을 돌면서 모든 코인들을 순회합니다.
    for ticker in Tickers:
        try:
            #캔들 정보를 가져와서 
            df = pyupbit.get_ohlcv(ticker,interval)

            #최근 2개 캔들의 종가와 거래량을 곱하여 대략의 거래대금을 구합니다.
            # 거래디금 = (오늘의 종가 * 현재거래량)으로 봐도 무방하다 
            # (오늘의 종가 * 현재거래량) + (어제 종가 * 어제거래량)
            # 오늘 거래대금 + 어제 거래대금
            volume_money = (df['close'].iloc[-1] * df['volume'].iloc[-1]) + (df['close'].iloc[-2] * df['volume'].iloc[-2])
           
            #volume_money = float(df['value'].iloc[-1]) + float(df['value'].iloc[-2]) #거래대금! value가 거래대금이었네요.. 이걸 이제야 알다니 ㅎ
            #이걸 위에서 만든 딕셔너리에 넣어줍니다. Key는 코인의 티커, Value는 위에서 구한 거래대금 
            dic_coin_money[ticker] = volume_money
            #출력해 봅니다.
            # print(ticker, dic_coin_money[ticker])
            #반드시 이렇게 쉬어줘야 합니다. 안그럼 에러가.. 시간조절을 해보시며 최적의 시간을 찾아보세요 전 일단 0.1로 수정했어요!
            time.sleep(0.1)

        except Exception as e:
            print("exception:",e)

    #딕셔너리를 값으로 정렬하되 숫자가 큰 순서대로 정렬합니다.
    dic_sorted_coin_money = sorted(dic_coin_money.items(), key = lambda x : x[1], reverse= True)

    #빈 리스트를 만듭니다.
    coin_list = list()

    #코인을 셀 변수를 만들어요.
    cnt = 0

    #티커와 거래대금 많은 순으로 정렬된 딕셔너리를 순회하면서 
    for coin_data in dic_sorted_coin_money:
        #코인 개수를 증가시켜주는데..
        cnt += 1

        #파라메타로 넘어온 top의 수보다 작으면 코인 리스트에 코인 티커를 넣어줍니다.
        #즉 top에 10이 들어갔다면 결과적으로 top 10에 해당하는 코인 티커가 coin_list에 들어갑니다.
        if cnt <= top:
            coin_list.append(coin_data[0])
        else:
            break

    print("--------------GetTopCoinList End-------------------")

    #코인 리스트를 리턴해 줍니다.
    return coin_list

#이동평균선 수치를 구해준다 첫번째: 분봉/일봉 정보, 두번째: 기간, 세번째: 기준 날짜
def GetMA(ohlcv,period,st):
    #이 역시 이동평균선을 제대로 구해줍니다.
    close = ohlcv["close"]
    ma = close.rolling(period).mean()
    return float(ma.iloc[st])

#해당되는 리스트안에 해당 코인이 있는지 여부를 리턴하는 함수
def CheckCoinInList(CoinList, Ticker):
    InCoinOk = False
 
    #리스트안에 해당 코인이 있는지 체크합니다.
    for coinTicker in CoinList:
        #있으면 True로!!
        if coinTicker == Ticker:
            InCoinOk = True
            break

    return InCoinOk

#티커에 해당하는 코인의 수익율을 구해서 리턴하는 함수.
def GetRevenueRate(balances,Ticker):
    revenue_rate = 0.0
    for value in balances:
        try:
            realTicker = value['unit_currency'] + "-" + value['currency']
            if Ticker == realTicker:
                time.sleep(0.05)
                
                #현재 가격을 가져옵니다.
                nowPrice = pyupbit.get_current_price(realTicker)

                #수익율을 구해서 넣어줍니다
                revenue_rate = (float(nowPrice) - float(value['avg_buy_price'])) * 100.0 / float(value['avg_buy_price'])
                break

        except Exception as e:
            print("GetRevenueRate error:", e)

    return revenue_rate

#티커에 해당하는 코인이 매수된 상태면 참을 리턴하는함수
def IsHasCoin(balances,Ticker):
    HasCoin = False
    for value in balances:
        realTicker = value['unit_currency'] + "-" + value['currency']
        if Ticker == realTicker:
            HasCoin = True
    return HasCoin

#내가 매수한 (가지고 있는) 코인 개수를 리턴하는 함수
def GetHasCoinCnt(balances):
    CoinCnt = 0
    for value in balances:
        avg_buy_price = float(value['avg_buy_price'])
        if avg_buy_price != 0: #원화, 드랍받은 코인(평균매입단가가 0이다) 제외!
            CoinCnt += 1
    return CoinCnt

#총 원금을 구한다!
def GetTotalMoney(balances):
    total = 0.0
    for value in balances:
        try:
            ticker = value['currency']
            if ticker == "KRW": #원화일 때는 평균 매입 단가가 0이므로 구분해서 총 평가금액을 구한다.
                total += (float(value['balance']) + float(value['locked']))
            else:
                avg_buy_price = float(value['avg_buy_price'])

                #매수평균가(avg_buy_price)가 있으면서 잔고가 0이 아닌 코인들의 총 매수가격을 더해줍니다.
                if avg_buy_price != 0 and (float(value['balance']) != 0 or float(value['locked']) != 0):
                    #balance(잔고 수량) + locked(지정가 매도로 걸어둔 수량) 이렇게 해야 제대로 된 값이 구해집니다.
                    #지정가 매도 주문이 없다면 balance에 코인 수량이 100% 있지만 지정가 매도 주문을 걸면 그 수량만큼이 locked로 옮겨지기 때문입니다.
                    total += (avg_buy_price * (float(value['balance']) + float(value['locked'])))
        except Exception as e:
            print("GetTotalMoney error:", e)
    return total

#총 평가금액을 구한다! 
#위 원금을 구하는 함수와 유사하지만 코인의 매수 평균가가 아니라 현재 평가가격 기준으로 총 평가 금액을 구한다.
def GetTotalRealMoney(balances):
    total = 0.0
    for value in balances:
        try:
            ticker = value['currency']
            if ticker == "KRW": #원화일 때는 평균 매입 단가가 0이므로 구분해서 총 평가금액을 구한다.
                total += (float(value['balance']) + float(value['locked']))
            else:
            
                avg_buy_price = float(value['avg_buy_price'])
                if avg_buy_price != 0 and (float(value['balance']) != 0 or float(value['locked']) != 0): #드랍받은 코인(평균매입단가가 0이다) 제외 하고 현재가격으로 평가금액을 구한다,.
                    realTicker = value['unit_currency'] + "-" + value['currency']

                    time.sleep(0.1)
                    nowPrice = pyupbit.get_current_price(realTicker)
                    total += (float(nowPrice) * (float(value['balance']) + float(value['locked'])))
        except Exception as e:
            print("GetTotalRealMoney error:", e)


    return total


if __name__ == "__main__":

    #내가 가진 잔고 데이터를 다 가져온다.
    balances = upbit.get_balances()

    TotalMoeny = GetTotalMoney(balances) # 총 원금
    TotalRealMoney = GetTotalRealMoney(balances) # 총 평가금액
    TotalRevenue = (TotalRealMoney - TotalMoeny) * 100.0/ TotalMoeny#내 총 수익율


    ## 파라미터 ## 
    #내가 매수할 총 코인 개수
    MaxCoinCnt = 5.0

    #처음 매수할 비중(퍼센트) 
    FirstRate = 10.0

    #추가 매수할 비중 (퍼센트)
    WaterRate = 5.0

    #코인당 매수할 최대 매수금액
    CoinMaxMoney = TotalMoeny / MaxCoinCnt

    #처음에 매수할 금액 10%
    FirstEnterMoney = CoinMaxMoney / 100.0 * FirstRate 

    #그 이후 매수할 금액 - 즉 물 탈 금액 5%
    WaterEnterMoeny = CoinMaxMoney / 100.0 * WaterRate

    print("-----------------------------------------------")
    print ("Total Money(총 원금):", TotalMoeny)
    print ("Total Real Money(총 평가금액):", TotalRealMoney)
    print ("Total Revenue(총 수익률)", TotalRevenue)
    print("-----------------------------------------------")
    print ("CoinMaxMoney(코인당 매수할 최대 매수금액): ", CoinMaxMoney)
    print ("FirstEnterMoney: ", FirstEnterMoney)
    print ("WaterEnterMoeny: ", WaterEnterMoeny)

    # 거래대금이 많은 탑코인 10개의 리스트
    TopCoinList = GetTopCoinList("week",10)

    # 제외할 코인들을 넣어두세요. 상폐예정이나 유의뜬 코인등등 원하는 코인을 넣어요! 
    DangerCoinList = ['KRW-MARO','KRW-TSHP','KRW-PXL']

    # 만약 나는 내가 원하는 코인만 지정해서 사고 싶다면 여기에 코인 티커를 넣고 아래 for문에서 LovelyCoinList를 활용하시면 되요!
    # LovelyCoinList = ['KRW-BTC','KRW-ETH','KRW-DOGE','KRW-DOT']

    # 원화마켓의 모든 코인 티커를 리스트로 받기
    Tickers = pyupbit.get_tickers("KRW")

    for ticker in Tickers:
        try:
            #거래량 많은 탑코인 리스트안의 코인이 아니라면 스킵! 탑코인에 해당하는 코인만 이후 로직을 수행한다.
            if CheckCoinInList(TopCoinList,ticker) == False:
                continue

            #위험한 코인이라면 스킵!!!
            if CheckCoinInList(DangerCoinList,ticker) == True:
                continue

            #나만의 러블리만 사겠다면 여기 주석을 풀고 위의 2부분을 주석처리 한다 
            #if CheckCoinInList(LovelyCoinList,ticker) == False:
            #    continue

            #이렇게 쉬어주는거 잊지 마세요!
            time.sleep(0.1)

            #60분봉 1시간봉 기준의 캔들 정보를 가져온다 
            df_60 = pyupbit.get_ohlcv(ticker,interval="minute60")

            #RSI지표를 구한다
            rsi60_min_before = GetRSI(df_60,14,-2) #이전 캔들 RSI지표
            rsi60_min = GetRSI(df_60,14,-1) #현재 캔들 RSI지표

            revenu_rate = GetRevenueRate(balances,ticker)
            print(ticker , ", RSI :", rsi60_min_before, " -> ", rsi60_min)

            #보유하고 있는 코인들 즉 매수 상태인 코인들
            if IsHasCoin(balances,ticker) == True:
                print("HasCoin")
                
                #수익율을 구해준다
                revenu_rate = GetRevenueRate(balances,ticker)
                print("revenu_rate: ",revenu_rate)

            #아직 매수하기 전인 코인들 즉 매수 대상
            # else: 
            #     print("No have")

        except Exception as e:
            print("error: ", e)




#얼만큼 코인을 사야 할까 11:50/16:51