import backtrader as bt
import yfinance as yf
from sqlalchemy import create_engine
import os
def runstrat(MyStrategy, strategy_name,date , engine,  ticker = 'BTC-USD' , cash = 100000, periodo = 1):
    """Runs the test

    Args:
        MyStrategy (list): List of strategies
        ticker (str, optional): YahooFinance type. Defaults to 'BTC-USD'.
        date (str): [description]. yyyy-mm-dd
        cash (int, optional): Defaults to 100000.
        Updates database with operations results.
    Returns:
        Returns cerebro with all its components
    """
    yyyy, mm, dd = int(date[:4])-periodo, int(date[5:7]),int(date[-2:])
    start = f'{yyyy}-{mm}-{dd}'
    
    df = yf.download(ticker,start, date)
    df.to_csv('datatester.csv')
    data = bt.feeds.YahooFinanceCSVData(dataname= 'datatester.csv')
    
    
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(cash)
    init_value = cerebro.broker.getvalue()
    #data = bt.feeds.BacktraderCSVData(dataname='../../datas/2006-day-001.txt')
    cerebro.adddata(data)
    
    cerebro.addobserver(bt.observers.DrawDown)

    cerebro.addstrategy(MyStrategy)
    cerebro.run()
    end_value = cerebro.broker.getvalue()
    return_pct = (end_value/init_value-1)*100
    
    print("Se comenzó con: ", init_value)
    print("Se terminó con: ",end_value)
    print("El retorno fue: ", return_pct,"%")
    #cerebro.plot()
    engine.execute(f"""insert into crypto_strategy_results (market,strategy_name, anual_return)
                                        values('{ticker}','{strategy_name}', {return_pct}) """)
    return cerebro