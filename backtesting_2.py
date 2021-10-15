import backtrader as bt
import yfinance as yf
import strategies


def runstrat(MyStrategy,ticker = 'BTC-USD',date =  '2021-01-01', cash = 100000):
    
    yyyy, mm, dd = int(date[:4])-1, int(date[5:7]),int(date[-2:])
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
    return_pct = end_value/init_value-1
    
    print("Se comenzó con: ", init_value)
    print("Se terminó con: ",end_value)
    print("El retorno fue: ", return_pct*100,"%")
    cerebro.plot()

if __name__ == '__main__':
    try:
        runstrat(strategies.smasCross, 'BTC-USD')
    except:
        print("Se produjo un error")










