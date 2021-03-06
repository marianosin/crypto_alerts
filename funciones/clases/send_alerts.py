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



class alerts():
    """Clase destinada a generalizar as alertas según activo y estrategia
    """
    
    def __init__(self,crypto_pair, ema):
        
        self.crypto = crypto_pair
        self.ema = ema
    def send_alert_emaPriceCross(self):
        """Envía notificaciones para el activo elegido y la ema elegida
        """
        pair = self.crypto
    # Descarga la base a python para chequear si hay una señal de compra 
        df = sqlio.read_sql_query(f"SELECT date, close_c, {self.ema}, rsi_14 from crypto_prices where coin_pair = '{pair}'", engine)
    #Grafica precio y ema 100
        plt.clf()
        plt.plot(df['date'], df['close_c'])
        plt.plot(df['date'], df[self.ema])
    #ajusta presencia
        plt.title(f"Precio de {self.crypto} vs EMA seleccionada")
        plt.xticks(rotation =90)
        plt.tight_layout()
        plt.savefig(f'images/adam_{self.crypto}.png')

        df_evaluation = df.tail(2)



        prev_price = df_evaluation.iloc[0,1]
        prev_ema = df_evaluation.iloc[0,2]
        prev_rsi = df_evaluation.iloc[0,3]

        last_price = df_evaluation.iloc[0,1]
        last_ema = df_evaluation.iloc[0,2]
        last_rsi = df_evaluation.iloc[0,3]

    #Falta crear las condiciones para evaluar y mandar el mensale
        msg = f"Activo: {self.crypto} \n Estrategia: {self.ema} "
        mensaje = {'username': 'Adam', 'content': msg}

        requests.post(os.environ.get('adam_ema100'), json= mensaje)

#Señal de compra
        if (prev_price<prev_ema) and (last_price>last_ema):
            msg = f"Señal: COMPRA \n Suceso: Cruce de precio a EMA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)
        #Señal de venta
        elif (prev_price>prev_ema) and (last_price<last_ema):
            msg = f"Señal: VENTA \n Suceso: Cruce de precio a EMA  \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)
        #Señal de mantener largo
        elif (prev_price>prev_ema) and (last_price>last_ema):
            msg = f"Señal: MANTENER LARGO \n Suceso: Precio por ENCIMA de EMA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get("adam_ema100"), json= mensaje)
        #Señal de mantener corto
        elif (prev_price<prev_ema) and (last_price<last_ema):
            msg = f"Señal: MANTENER CORTO \n Suceso: Precio por DEBAJO de EMA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)
        #Próximo a sobre compra
        if (65<last_rsi<70):
            msg = f"Señal: Preparar VENTA \n Suceso: RSI próximo a SOBRE COMPRA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)
        elif (70<=last_rsi):
            msg = f"Señal: PRECIO EN ZONA DE SOBRE COMPRA \n Suceso: RSI EN SOBRE COMPRA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)    
        #Proximo a sobre venta
        elif (30<last_rsi<35):
            msg = f"Señal: Preparar COMPRA \n Suceso: RSI próximo a SOBRE VENTA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)
        elif (last_rsi<=30):
            msg = f"Señal: PRECIO EN ZONA DE SOBRE VENTA \n Suceso: RSI EN SOBRE VENTA \n Último precio de cierre: {last_price} \n RSI {last_rsi} "
            mensaje = {'username': 'Adam', 'content': msg}

            requests.post(os.environ.get('adam_ema100'), json= mensaje)  
        msg = f"Se adjuntan los gráficos actualizados de precio, EMA y RSI."
        mensaje = {'username': 'Adam', 'content': msg}
        requests.post(os.environ.get("adam_ema100"), json= mensaje)
        plt.clf()
        plt.plot(df['date'], df['rsi_14'])
        #ajusta presencia
        plt.title(f"RSI de {self.crypto} ")
        plt.xticks(rotation =90)
        plt.axhline(70, color = 'red')
        plt.axhline(65, color = 'red')
        plt.axhline(35, color = 'green')
        plt.axhline(30, color = 'green')
        plt.tight_layout()
        plt.savefig(f'images/adam_rsi_{self.crypto}.png')

        requests.post(os.environ.get("adam_ema100"), json= mensaje, files= {'upload_file': open(f'images/adam_{self.crypto}.png','rb')} )
        requests.post(os.environ.get("adam_ema100"), json= mensaje, files= {'upload_file': open(f'images/adam_rsi_{self.crypto}.png','rb')} )
