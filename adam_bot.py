import discord
import requests
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine
#Conección a la base de datos
user = os.environ.get("db_user")
password = os.environ.get("db_pass")
host = os.environ.get("db_host")
engine = create_engine(f'postgresql://{user}:{password}@{host}/tablero_acciones')


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


#Señal de compra
if (prev_price<prev_ema) and (last_price>last_ema):
    msg = f"Señal: COMPRA \n Suceso: Cruce de precio a EMA de 100 \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)
#Señal de venta
elif (prev_price>prev_ema) and (last_price<last_ema):
    msg = f"Señal: VENTA \n Suceso: Cruce de precio a EMA de 100 \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)
#Señal de mantener largo
elif (prev_price>prev_ema) and (last_price>last_ema):
    msg = f"Señal: MANTENER LARGO \n Suceso: Precio por ENCIMA de EMA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get("adam_ema100"), json= mensaje)
#Señal de mantener corto
elif (prev_price<prev_ema) and (last_price<last_ema):
    msg = f"Señal: MANTENER CORTO \n Suceso: Precio por DEBAJO de EMA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)
#Próximo a sobre compra
if (65<last_rsi<70):
    msg = f"Señal: Preparar VENTA \n Suceso: RSI próximo a SOBRE COMPRA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)
elif (70<=last_rsi):
    msg = f"Señal: PRECIO EN ZONA DE SOBRE COMPRA \n Suceso: RSI EN SOBRE COMPRA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)    
#Proximo a sobre venta
elif (30<last_rsi<35):
    msg = f"Señal: Preparar COMPRA \n Suceso: RSI próximo a SOBRE VENTA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)
elif (last_rsi<=30):
    msg = f"Señal: PRECIO EN ZONA DE SOBRE VENTA \n Suceso: RSI EN SOBRE VENTA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
    mensaje = {'username': 'Adam', 'content': msg}

    requests.post(os.environ.get('adam_ama100'), json= mensaje)  
msg = f"Se adjuntan los gráficos actualizados de precio, EMA y RSI."
mensaje = {'username': 'Adam', 'content': msg}
requests.post(os.environ.get("adam_ema100"), json= mensaje)
plt.clf()
plt.plot(df['date'], df['rsi_14'])
#ajusta presencia
plt.title("RSI de BTC-USDT")
plt.xticks(rotation =90)
plt.axhline(70, color = 'red')
plt.axhline(65, color = 'red')
plt.axhline(35, color = 'green')
plt.axhline(30, color = 'green')
plt.tight_layout()
plt.savefig('images/adam_rsi_btc-usdt.png')

requests.post(os.environ.get("adam_ema100"), json= mensaje, files= {'upload_file': open('images/adam_btc-usdt.png','rb')} )
requests.post(os.environ.get("adam_ema100"), json= mensaje, files= {'upload_file': open('images/adam_rsi_btc-usdt.png','rb')} )