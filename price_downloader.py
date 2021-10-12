import ccxt
import os 
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import pandas_ta as ta
import pandas.io.sql as sqlio
from funciones.conecta_db import conecta_db

# Conecta a base de datos 
engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')

# Conecta proveedor de datos
exchange = ccxt.binance()

# markets = exchange.load_markets()
# for i in markets:
#     if 'BTC' in i:
#         print(i)

# Descarga pares de interes
pairs = sqlio.read_sql('SELECT * FROM crypto_makets', conecta_db('tablero_acciones') )

engine.execute('drop table crypto_prices;')
for pair in pairs.market_pair:

    ohlc_btcusdt = exchange.fetch_ohlcv(pair, timeframe='1d')


    # Calcula los indicadores de interés
    df = pd.DataFrame(ohlc_btcusdt, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df['Time'] = [datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
    df.set_index('Time', inplace=True)
    df['coin_pair'] = pair
    ema10 = ta.ema(df["Close"], length=10)
    df['ema_10'] = ema10
    ema10 = ta.ema(df["Close"], length=10)
    df['ema_10'] = ema10
    ema20 = ta.ema(df["Close"], length=20)
    df['ema_20'] = ema20
    ema50 = ta.ema(df["Close"], length=50)
    df['ema_50'] = ema50
    ema200 = ta.ema(df["Close"], length=200)
    df['ema_200'] = ema200
    rsi14 = ta.rsi(df["Close"], length=14)
    df['rsi_14'] = rsi14
    df['lower_band'] = ta.bbands(df['Close'])["BBL_5_2.0"]
    df['upper_band'] = ta.bbands(df['Close'])["BBU_5_2.0"]
    df['mid_band'] = ta.bbands(df['Close'])["BBM_5_2.0"]

    
    df.to_sql('crypto_prices',con=engine , if_exists='append', index=True)
    print(pair, 'Ok')
# # for i in df.shape[0]:
    

# # df['bbands_signals']

# # print(df.tail(20))