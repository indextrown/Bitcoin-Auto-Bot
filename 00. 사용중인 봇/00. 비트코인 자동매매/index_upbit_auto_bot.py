# [made by index]
# rsi60분봉 기준으로 30이하일 때 분할매수 진행
# (15분마다 크론탭) == 4번의 매수 기회 생김
# (10분마다 크론탭) == 6번의 매수 기회 생김
# (5분마다 크론탭) == 12번의 매수 기회 생김

# (15분마다 크론탭) == 4번의 매수 기회 생김 -> 이걸로 진행예정
# 현재 실시간 값을 반영하기 때문에 4번 의 매수기회가 있어도 4번 다 확정으로 매수되는건 아님

# 하락장에서는 최대한 매수할 금액을 남겨두는 것이 전략!
# 수익 3퍼센트만 나도 무조건 판매도 전략!
# rsi 70이상이더라도 수익이 나면 판매하는것도 전략!
# 계속 낮아지는 하락장에서 만약 물탈 돈이 없다(원금 바닥남) => 매수한 코인 중에 하나를 절반을 팔자
# => (수익률 -10퍼센트 이상이면 내가 가진 코인 중 하나를 절반을 팔자 이러면 물탈 돈 생김)
# 즉 한개의 코인을 팔아서 물탈돈 마련해서 물을 타는 것이 평균 단가를 낮춰주는게 나을 수 있다
# https://class101.net/ko/classes/60dab8da41daac0014f1d4fa/lectures/60e11033659fd100143310ca
# https://blog.naver.com/zacra/223170880153
# https://blog.naver.com/zacra/223049832963

import time
import pandas as pd
import pyupbit
from dotenv import load_dotenv
import os
import pandas as pd
from myUpbit import *
#챕터7까지 진행하시면서 봇은 점차 완성이 되어 갑니다!!!
#챕터5까지 완강 후 봇을 돌리셔도 되지만 이왕이면 7까지 완강하신 후 돌리시는 걸 추천드려요!

# load .env
load_dotenv()

# key
Access_Key = os.environ.get('Access_Key')
Secret_Key = os.environ.get('Secret_Key')

#업비트 객체를 만들어요 액세스 키와 시크릿 키를 넣어서요.
upbit = pyupbit.Upbit(Access_Key, Secret_Key)


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
    print ("Total Real Money(현재 평가 금액):", TotalRealMoney)
    print ("Total Revenue(총 수익률)", TotalRevenue)
    print("-----------------------------------------------")
    print ("CoinMaxMoney(코인당 매수할 최대 금액): ", CoinMaxMoney)
    print ("FirstEnterMoney(처음 매수할 금액): ", FirstEnterMoney)
    print ("WaterEnterMoeny(추가매수(물탈)금액): ", WaterEnterMoeny)

    # 거래대금이 많은 탑코인 10개의 리스트
    TopCoinList = GetTopCoinList("week",10)

    # 제외할 코인들을 넣어두세요. 상폐예정이나 유의뜬 코인등등 원하는 코인을 넣어요! 
    DangerCoinList = ['KRW-MARO','KRW-TSHP','KRW-PXL', 'KRW-BTC', 'KRW-BTG']

    # 만약 나는 내가 원하는 코인만 지정해서 사고 싶다면 여기에 코인 티커를 넣고 아래 for문에서 LovelyCoinList를 활용하시면 되요!
    # LovelyCoinList = ['KRW-BTC','KRW-ETH','KRW-DOGE','KRW-DOT']

    # 원화마켓의 모든 코인 티커를 리스트로 받기
    Tickers = pyupbit.get_tickers("KRW")

    for ticker in Tickers:
        try:
            """ [매수된 코인들] """
            #보유하고 있는 코인들 즉 매수 상태인 코인들
            if IsHasCoin(balances,ticker) == True:

                #위험한 코인이라면 스킵!!!
                if CheckCoinInList(DangerCoinList,ticker) == True:
                    continue

                # print("!!!!! 내 전략에 맞는 매수매도 대상 코인 :",ticker)

                #이렇게 쉬어주는거 잊지 마세요!
                time.sleep(0.1)

                #60분봉 1시간봉 기준의 캔들 정보를 가져온다 
                df_60 = pyupbit.get_ohlcv(ticker,interval="minute60")

                #RSI지표를 구한다
                rsi60_min_before = GetRSI(df_60,14,-3) #이전 캔들 RSI지표
                rsi60_min = GetRSI(df_60,14,-2) #현재 캔들 RSI지표

                revenu_rate = GetRevenueRate(balances,ticker)
                print(ticker , ", RSI :", rsi60_min_before, " -> ", rsi60_min)

                # 원화 잔고를 가져온다
                won = float(upbit.get_balance("KRW"))

                # 수익율을 구한다.
                revenu_rate = GetRevenueRate(balances,ticker)

                print("# Remain Won :", won)
                print("------------------------------------")
                print("Coin ticker :",ticker)
                print("- Recently RSI :", rsi60_min_before, " -> ", rsi60_min)
                print("- Now Revenue : ",revenu_rate)


                # 현재 코인의 총 매수금액
                NowCoinTotalMoney = GetCoinNowMoney(balances,ticker)

                # 그냥 수익률이 생기면 바로바로 분할매도하려면 이방식
                #if revenu_rate > 1.0

                """ [매도 로직] """
                # rsi 70 이상이면서 수익률 1%이상이라면
                # if rsi60_min >= 70.0 and revenu_rate >= 1.0:

                # 70까지 안가고 고점찍고 하락가는게 걱정되면 or로 바꾸면됨
                if rsi60_min >= 70.0 and revenu_rate >= 1.0:
                    
                    # 60분봉 기준 15분마다 스케줄러 돌려서 4번 안에 다 분할매도 하기 위해
                    # 최대 코인 매수 금액 / 4.0 = 25% 까지는 그냥 팔아버리고 그 이상일 경우는 분할매도 하겠다

                    # 최대코인매수금액의 1/4보다 작다면 전체 시장가 매도 
                    if NowCoinTotalMoney < (CoinMaxMoney / 4.0):    
                        print(f"Debug: [전량 매도] 매수 금액이 최대 금액의 25% 이하")
                        print(upbit.sell_market_order(ticker,upbit.get_balance(ticker)))

                    # 최대코인매수금액의 1/4보다 크다면 절반씩 시장가 매도 
                    else:
                        print(f"Debug: [절반 매도] 매수 금액이 최대 금액의 25% 초과")
                        print(upbit.sell_market_order(ticker, upbit.get_balance(ticker) / 2.0)) # 절반씩 매도

                    time.sleep(2.0)

                    #팔았으면 원화를 다시 가져올 필요가 있다.
                    won = float(upbit.get_balance("KRW"))
                
                # [손절하기 싫고 존버하고 싶으면 빼도 됨]
                # 내가 가진 원화가 물탈 돈보다 적다..(원금 바닥) 그런데 수익율이 - 10% 이하다? 그럼 절반 팔아서 물탈돈을 마련하자!
                if won < WaterEnterMoeny and revenu_rate <= -10.0:
                    print(f"Debug: [손절] 원화 잔고 부족 및 수익률 -10% 이하 즉 절반 매도")
                    print(upbit.sell_market_order(ticker,upbit.get_balance(ticker) / 2.0))
 
                # 예시: 수익률 -20%이면 전체매도
                # if revenu_rate < -20:
                #    print(upbit.sell_market_order(ticker,upbit.get_balance(ticker)))

                # 할당된 최대코인매수금액 대비 매수된 코인 비율
                Total_Rate = NowCoinTotalMoney / CoinMaxMoney * 100.0

                """ [매수 로직] """
                # 60분봉 기준 RSI지표 30 이하일때 
                # if rsi60_min <= 30.0:

                # 60분봉 기준 RSI지표 30 이하에서 빠져나왔을 때
                if rsi60_min_before <= 30.0 and rsi60_min > 30.0:
                     
                    # 할당된 최대코인매수금액 대비 매수된 코인 비중이 50%이하일때.. 물타기 진행
                    if Total_Rate <= 50.0:
                        time.sleep(0.05)
                        print(upbit.buy_market_order(ticker,WaterEnterMoeny))

                    # 50%를 초과하면
                    else:
                        #수익율이 마이너스 5% 이하 일때만 매수를 진행하여 원금 소진을 늦춘다.
                        if revenu_rate <= -5.0:
                            time.sleep(0.05)
                            print(upbit.buy_market_order(ticker,WaterEnterMoeny))



            # 아직 매수하기 전인 코인들 즉 매수 대상
            else: 
                #거래량 많은 탑코인 리스트안의 코인이 아니라면 스킵! 탑코인에 해당하는 코인만 이후 로직을 수행한다.
                if CheckCoinInList(TopCoinList,ticker) == False:
                    continue

                #위험한 코인이라면 스킵!!!
                if CheckCoinInList(DangerCoinList,ticker) == True:
                    continue

                #나만의 러블리만 사겠다면 여기 주석을 풀고 위의 2부분을 주석처리 한다 
                #if CheckCoinInList(LovelyCoinList,ticker) == False:
                #    continue

                # print("!!!!! 내 전략에 맞는 매수매도 대상 코인 :",ticker)

                #이렇게 쉬어주는거 잊지 마세요!
                time.sleep(0.1)

                #60분봉 1시간봉 기준의 캔들 정보를 가져온다 
                df_60 = pyupbit.get_ohlcv(ticker,interval="minute60")

                #RSI지표를 구한다
                rsi60_min_before = GetRSI(df_60,14,-3) #이전 캔들 RSI지표
                rsi60_min = GetRSI(df_60,14,-2) #현재 캔들 RSI지표


                print("------------------------------------")
                print("Coin ticker :",ticker)
                print("- Recently RSI :", rsi60_min_before, " -> ", rsi60_min)


                """ [매수안된 코인들] """
                #60분봉 기준 RSI지표 30 이하이면서 아직 매수한 코인이 MaxCoinCnt보다 작다면 매수 진행!
                
                # if rsi60_min <= 30.0 and GetHasCoinCnt(balances) < MaxCoinCnt:
                """ [매수 로직] """
                #60분봉 기준 RSI지표 30 이하에서 빠져나온면서 아직 매수한 코인이 MaxCoinCnt보다 작다면 매수 진행!
                if rsi60_min_before <= 30.0 and rsi60_min > 30.0 and GetHasCoinCnt(balances) < MaxCoinCnt :
                    time.sleep(0.05)
                    print(f"Debug: [RSI 매수 조건 충족] Ticker: {ticker}")
                    print(upbit.buy_market_order(ticker,FirstEnterMoney))
                    
                """ [단타 로직] """
                time.sleep(0.05)
                df_15 = pyupbit.get_ohlcv(ticker,interval="minute15") #15분봉 데이타를 가져온다.

                #15분봉 기준 5일선 값을 구한다.
                ma5_before3 = GetMA(df_15,5,-4)
                ma5_before2 = GetMA(df_15,5,-3)
                ma5 = GetMA(df_15,5,-2)

                #15분봉 기준 20일선 값을 구한다.
                ma20 = GetMA(df_15,20,-2)

                print("ma20 :", ma20)
                print("ma5 :", ma5 , " <- ", ma5_before2, " <- ", ma5_before3)

                #5일선이 20일선 밑에 있을 때 5일선이 상승추세로 꺽이면 매수를 진행하자!!
                if ma5 < ma20 and ma5_before3 > ma5_before2 and ma5_before2 < ma5 and GetHasCoinCnt(balances) < MaxCoinCnt:
                    print(f"Debug: [단타 매수 조건 충족] Ticker: {ticker}")
                    #시장가 매수를 한다.
                    balances = BuyCoinMarket(upbit,ticker,FirstEnterMoney)

                    #평균매입단가와 매수개수를 구해서 1% 상승한 가격으로 지정가 매도주문을 걸어놓는다.
                    avgPrice = GetAvgBuyPrice(balances,ticker)
                    coin_volume = upbit.get_balance(ticker)

                    avgPrice *= 1.01

                    #지정가 매도를 한다.
                    print("지정가 매도 시작", ticker)
                    print(f"Debug: [지정가 매도 설정] 목표가: {avgPrice}, 매도 수량: {coin_volume}")
                    SellCoinLimit(upbit,ticker,avgPrice,coin_volume)

                #이부분이 이번 강의에서 추가 되었지만 사실 해당 봇이 1분마다 돌지 않는 한 15분씩 도는 봇에 1분봉을 보는 것은 큰 의미가 없습니다. 이는 이후 강의에서 수정(분리)되니 참고하세요!
                """
                """
                
        except Exception as e:
            print("error: ", e)



#얼만큼 코인을 사야 할까 11:50/16:51






#이부분이 이번 강의에서 추가 되었지만 사실 해당 봇이 1분마다 돌지 않는 한 15분씩 도는 봇에 1분봉을 보는 것은 큰 의미가 없습니다. 이는 이후 강의에서 수정(분리)되니 참고하세요!
"""
time.sleep(0.05)
df_1 = pyupbit.get_ohlcv(ticker,interval="minute1") #1분봉 데이타를 가져온다.

rsi1_min = GetRSI(df_1,14,-1)
print("-rsi1_min:", rsi1_min)

#1분봉 기준으로 30이하일때 매수를 한다.
if rsi1_min < 30.0 and GetHasCoinCnt(balances) < MaxCoinCnt:
print("!!!!!!!!!!!!!!!DANTA DANTA RSI First Buy GoGoGo!!!!!!!!!!!!!!!!!!!!!!!!")
#시장가 매수를 한다.
balances = BuyCoinMarket(upbit,ticker,FirstEnterMoney)

#평균매입단가와 매수개수를 구해서 1% 상승한 가격으로 지정가 매도주문을 걸어놓는다.
avgPrice = GetAvgBuyPrice(balances,ticker)
coin_volume = upbit.get_balance(ticker)

avgPrice *= 1.01

#지정가 매도를 한다.
SellCoinLimit(upbit,ticker,avgPrice,coin_volume)
"""
