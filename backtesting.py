import backtrader as bt
from backtrader import position
import pandas.io.sql as sqlio
from sqlalchemy import create_engine
import os
import pandas as pd
import datetime
cerebro = bt.Cerebro()

engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')


cerebro.broker.set_cash(100000)

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period= 14)
    
    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=0.0001)
        if self.rsi > 70 and self.position:
            self.close()
            
# class SmaCross(bt.Strategy):
#     # list of parameters which are configurable for the strategy
#     params = dict(
#         pfast=10,  # period for the fast moving average
#         pslow=50   # period for the slow moving average
#     )

#     def __init__(self):
#         sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
#         sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
#         self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

#     def next(self):
    
#         if self.crossover > 0:  # if fast crosses slow to the upside
        
#             self.close()
#             print(self.position)
#             self.buy() # enter long
#             print("Buy {} shares".format( self.data.close[0]))
#             print(self.position)
                

#         elif self.crossover < 0:  # in the market & cross to the downside

#             self.close()# close long position
#             print(self.position)
#             self.sell()
#             print("Sale {} shares".format(self.data.close[0]))
#             print(self.position)


data = sqlio.read_sql("select date_c, open_c, high_c, low_c, close_c from crypto_prices where coin_pair ='BTC/USDT'", con = engine, index_col='date_c')
data.to_csv('data/backtesting.csv')
#df = bt.feeds.PandasData(dataname=data)
df = bt.feeds.GenericCSV(dataname= 'data/backtesting.csv', dtformat= lambda x: datetime.datetime.utcfromtimestamp(float(x) / 1000.0))



cerebro.adddata(df)
cerebro.addstrategy(RSIStrategy)
cerebro.run()
cerebro.plot()