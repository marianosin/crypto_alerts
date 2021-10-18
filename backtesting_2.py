import backtrader as bt
import yfinance as yf
import strategies
from funciones.run_backtest import runstrat
from funciones.save_backtrader_plot import saveplots
from datetime import date, datetime
strat = [strategies.RSIStrategy,strategies.BOLLStrat, strategies.BOLLRSIStrat, strategies.emaPriceCross, strategies.smasCross, strategies.smaCross]
stname = ["RSI","BOLL", "BOLLRSI","EMACROSS","SMAsCROSS", "SMACROSS"]
markets = ["BTC-USD", "ADA-USD","ETH-USD", "LTC-USD", "BNB-USD"]
def backtester(date = '2021-10-18', strat = [strategies.RSIStrategy,strategies.BOLLStrat, strategies.BOLLRSIStrat, strategies.emaPriceCross, strategies.smasCross, strategies.smaCross], stname = ["RSI","BOLL", "BOLLRSI","EMACROSS","SMAsCROSS", "SMACROSS"], markets = ["BTC-USD", "ADA-USD","ETH-USD", "LTC-USD", "BNB-USD"]):
    for st in strat:
        for name in stname:
            for market in markets:
                print("Estrategia: ", name)
                print("Mercado: ", market)
                print("*"*40)
                saveplots(runstrat(st, date = date, ticker= market), file_path= f'images/backtest_{name}_{market}.png')











