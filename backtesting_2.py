import backtrader as bt
import yfinance as yf
import strategies
from funciones.run_backtest import runstrat
from funciones.save_backtrader_plot import saveplots


if __name__ == '__main__':
    try:
        saveplots(runstrat(strategies.BOLLStrat, 'BTC-USD'), file_path= 'images/backtest_imp.png')
    except:
        print("Se produjo un error")










