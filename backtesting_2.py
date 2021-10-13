import backtrader as bt
import yfinance as yf
import strategies

ticker = 'BTC-USD'
start =  '2021-01-01'
end = '2021-10-11'
df = yf.download(ticker,start, end)
df.to_csv('datatester.csv')


cerebro = bt.Cerebro()
cerebro.addstrategy(strategies.emaPriceCross)
cerebro.broker.set_cash(100000)


data = bt.feeds.YahooFinanceCSVData(dataname= 'datatester.csv')

cerebro.adddata(data)
cerebro.run()
cerebro.plot()