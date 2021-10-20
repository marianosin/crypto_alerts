
import strategies
from funciones.run_backtest import runstrat
from funciones.save_backtrader_plot import saveplots

strat = [strategies.RSIStrategy,strategies.BOLLStrat, strategies.BOLLRSIStrat, strategies.emaPriceCross, strategies.smasCross, strategies.smaCross]
stname = ["RSI","BOLL", "BOLLRSI","EMACROSS","SMAsCROSS", "SMACROSS"]
markets = ["BTC-USD", "ADA-USD","ETH-USD", "LTC-USD", "BNB-USD"]


def run_saveplot_strategy(strategy, ticker, strategy_name, date, engine, file_name):
    

    saveplots(runstrat(strategy, strategy_name=strategy_name, date= date, engine= engine, ticker= ticker),file_path=file_name)

