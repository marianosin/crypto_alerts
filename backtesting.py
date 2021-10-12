import backtrader as bt
import pandas.io.sql as sqlio
from sqlalchemy import create_engine
import os
import pandas as pd
cerebro = bt.Cerebro()

engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')


cerebro.broker.set_cash(10000)


class PandasData(bt.feeds.PandasData):
    lines = ('adj_close','ema_10','ema_20','ema_50', 'ema_200', 'rsi_14', 'lower_band', 'upper_band', 'mid_band', 'Time')
    params = (
        ('datetime', None),
        ('open','Open'),
        ('high','High'),
        ('low','Low'),
        ('close','Close'),
        ('volume','Volume'),
        ('openinterest',None),
        ('adj_close',None),
        ('ema_10','ema_10'),
        ('ema_20','ema_20'),
        ('ema_50','ema_50'),
        ('ema_200','ema_200'),
        ('rsi_14','rsi_14'),
        ('lower_band','lower_band'),
        ('upper_band','upper_band'),
        ('mid_band','mid_band'),
        ('Time', 'Time')
    )

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=50   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
    
        if self.crossover > 0:  # if fast crosses slow to the upside
        
            self.close()
            print(self.position)
            self.buy() # enter long
            print("Buy {} shares".format( self.data.close[0]))
            print(self.position)
                

        elif self.crossover < 0:  # in the market & cross to the downside

            self.close()# close long position
            print(self.position)
            self.sell()
            print("Sale {} shares".format(self.data.close[0]))
            print(self.position)


data = sqlio.read_sql("select * from crypto_prices where coin_pair ='BTC/USDT'", con = engine, index_col='Time')

#df = bt.feeds.PandasData(dataname=data)
df=PandasData(dataname=data)

cerebro.adddata(df)
cerebro.addstrategy(SmaCross)
cerebro.run()
cerebro.plot()