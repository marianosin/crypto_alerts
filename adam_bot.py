import discord
import requests
import pandas.io.sql as sqlio
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine

#Clases propias

from funciones.clases.send_alerts import alerts



#Conección a la base de datos
user = os.environ.get("db_user")
password = os.environ.get("db_pass")
host = os.environ.get("db_host")
engine = create_engine(f'postgresql://{user}:{password}@{host}/tablero_acciones')


#Sistema de notificaciones




adam = alerts('BTC-USDT', 'ema_100')
adam.send_alert_emaPriceCross()
adam = alerts('ETH-USDT', 'ema_100')
adam.send_alert_emaPriceCross()
adam = alerts('ADA-USDT', 'ema_100')
adam.send_alert_emaPriceCross()