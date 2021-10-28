"""Descarga los datos con los que posteriormente se notificará al usuario.
"""

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
pairs = sqlio.read_sql('SELECT * FROM crypto_markets', conecta_db('tablero_acciones') )

engine.execute('drop table crypto_prices;')
for pair in pairs.market_pair:

    ohlc_btcusdt = exchange.fetch_ohlcv(pair, timeframe='1d')


    # Calcula los indicadores de interés
    df = pd.DataFrame(ohlc_btcusdt, columns = ['date', 'open_c', 'high_c', 'low_c', 'close_c', 'volume_c'])
    df['date'] = [datetime.fromtimestamp(float(time)/1000) for time in df['date']]
    # df['date_c'] = [(float(time)/1) for time in df['date_c']]
    df.set_index('date', inplace=True)
    df['coin_pair'] = pair.replace('/','-')
    ema10 = ta.ema(df["close_c"], length=10)
    df['ema_10'] = ema10
    ema10 = ta.ema(df["close_c"], length=10)
    df['ema_10'] = ema10
    ema20 = ta.ema(df["close_c"], length=20)
    df['ema_20'] = ema20
    ema50 = ta.ema(df["close_c"], length=50)
    df['ema_50'] = ema50
    ema100 = ta.ema(df["close_c"], length=100)
    df['ema_100'] = ema100
    ema200 = ta.ema(df["close_c"], length=200)
    df['ema_200'] = ema200
    rsi14 = ta.rsi(df["close_c"], length=14)
    df['rsi_14'] = rsi14
    df['lower_band'] = ta.bbands(df['close_c'])["BBL_5_2.0"]
    df['upper_band'] = ta.bbands(df['close_c'])["BBU_5_2.0"]
    df['mid_band'] = ta.bbands(df['close_c'])["BBM_5_2.0"]

    
    df.to_sql('crypto_prices',con=engine , if_exists='append', index=True)
    print(pair, 'Ok')
# # for i in df.shape[0]:
    

# # df['bbands_signals']

# # print(df.tail(20))