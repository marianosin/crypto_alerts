import discord
import requests
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine
#Conección a la base de datos
engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')


#Sistema de notificaciones



mensaje = {'username': 'Adam', 'content': "Hola"}

# Descarga la base a python para chequear si hay una señal de compra 
df = sqlio.read_sql_query("SELECT date, close_c, ema_100, rsi_14 from crypto_prices where coin_pair = 'BTC-USDT'", engine)
#Grafica precio y ema 100
plt.plot(df['date'], df['close_c'])
plt.plot(df['date'], df['ema_100'])
#ajusta presencia
plt.title("Precio de BTC-USDT vs EMA 100")
plt.xticks(rotation =90)
plt.tight_layout()
plt.savefig('images/adam_btc-usdt.png')

df_evaluation = df.tail(2)



prev_price = df_evaluation.iloc[0,1]
prev_ema = df_evaluation.iloc[0,2]
prev_rsi = df_evaluation.iloc[0,3]

last_price = df_evaluation.iloc[0,1]
last_ema = df_evaluation.iloc[0,2]
last_rsi = df_evaluation.iloc[0,3]

#Falta crear las condiciones para evaluar y mandar el mensale






#requests.post(os.environ.get("adam_ema100"), json= mensaje)

