import backtrader as bt
import datetime



class BOLLRSIStrat(bt.Strategy):
     
    '''
    Combina Bollinger y RSI
    '''

    params = (
        ("period", 20),
        ("devfactor", 2),
        ("size", 20),
        ("debug", False)
        )

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        self.rsi = bt.ind.RSI(self.data, period= 14)
        #self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        #self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
        self.str_name = "BOLLRSI"

    def next(self):

        orders = self.broker.get_orders_open()

        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)

        if not self.position:

            if (self.data.close > self.boll.lines.top) or (self.rsi>70):

                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)

            if (self.data.close < self.boll.lines.bot) and (self.rsi>30):
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)

        else:

            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            print("1: Data Name:                            {}".format(data._name))
            print("2: Bar Num:                              {}".format(len(data)))
            print("3: Current date:                         {}".format(data.datetime.datetime()))
            print('4: Open:                                 {}'.format(data.open[0]))
            print('5: High:                                 {}'.format(data.high[0]))
            print('6: Low:                                  {}'.format(data.low[0]))
            print('7: Close:                                {}'.format(data.close[0]))
            print('8: Volume:                               {}'.format(data.volume[0]))
            print('9: Position Size:                       {}'.format(self.position.size))
            print('--------------------------------------------------------------------')

    # def notify_trade(self,trade):
    #     if trade.isclosed:
    #         dt = self.data.datetime.date()

    #         print('---------------------------- TRADE ---------------------------------')
    #         print("1: Data Name:                            {}".format(trade.data._name))
    #         print("2: Bar Num:                              {}".format(len(trade.data)))
    #         print("3: Current date:                         {}".format(dt))
    #         print('4: Status:                               Trade Complete')
    #         print('5: Ref:                                  {}'.format(trade.ref))
    #         print('6: PnL:                                  {}'.format(round(trade.pnl,2)))
    #         print('--------------------------------------------------------------------')


class BOLLStrat(bt.Strategy):

    '''
    Estrategia con Bollinger bands
    '''

    params = (
        ("period", 20),
        ("devfactor", 2),
        ("size", 20),
        ("debug", False)
        )

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        #self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        #self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)
        self.str_name = "BOLL"
    def next(self):

        orders = self.broker.get_orders_open()

        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)

        if not self.position:

            if self.data.close > self.boll.lines.top:

                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0], size=self.p.size)

            if self.data.close < self.boll.lines.bot:
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0], size=self.p.size)

        else:

            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)

        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            print("1: Data Name:                            {}".format(data._name))
            print("2: Bar Num:                              {}".format(len(data)))
            print("3: Current date:                         {}".format(data.datetime.datetime()))
            print('4: Open:                                 {}'.format(data.open[0]))
            print('5: High:                                 {}'.format(data.high[0]))
            print('6: Low:                                  {}'.format(data.low[0]))
            print('7: Close:                                {}'.format(data.close[0]))
            print('8: Volume:                               {}'.format(data.volume[0]))
            print('9: Position Size:                       {}'.format(self.position.size))
            print('--------------------------------------------------------------------')

    # def notify_trade(self,trade):
    #     if trade.isclosed:
    #         dt = self.data.datetime.date()

    #         print('---------------------------- TRADE ---------------------------------')
    #         print("1: Data Name:                            {}".format(trade.data._name))
    #         print("2: Bar Num:                              {}".format(len(trade.data)))
    #         print("3: Current date:                         {}".format(dt))
    #         print('4: Status:                               Trade Complete')
    #         print('5: Ref:                                  {}'.format(trade.ref))
    #         print('6: PnL:                                  {}'.format(round(trade.pnl,2)))
    #         print('--------------------------------------------------------------------')




class smaCross(bt.SignalStrategy):
    def __init__(self):
        sma =  bt.ind.SMA(period=50)
        price = self.data
        crossover = bt.ind.CrossOver(price, sma)
        self.signal_add(bt.SIGNAL_LONG, crossover)
        self.str_name = "SMACross"

class smasCross(bt.SignalStrategy):
    """Estrategias con cruce de medias móviles"""
    def __init__(self):
        ema1 =  bt.ind.SMA(period=20)
        ema2 = bt.ind.SMA(period=100)
        self.str_name = "SMAsCross"
        crossover = bt.ind.CrossOver(ema1, ema2)
        self.signal_add(bt.SIGNAL_LONG, crossover)
class emaPriceCross(bt.SignalStrategy):
    """Estrategia con ema y precio

    Args:
        bt ([type]): [description]
    """
    def __init__(self):
        
        self.ema1 =  bt.ind.EMA(period= 100)
        self.price = self.data
        self.rsi = bt.ind.RSI(self.data, period= 14)
        self.str_name = "EMACross"
        crossover = bt.ind.CrossOver(self.price, self.ema1)
        self.signal_add(bt.SIGNAL_LONG, crossover)




class RSIStrategy(bt.Strategy):
    """Estrategia con RSI

    Args:
        bt ([type]): [description]
    """
    def __init__(self):
        
        self.rsi = bt.ind.RSI(self.data, period= 14)
        self.str_name = "RSI"
    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=1)
        if self.rsi > 70 and self.position:
            self.close()