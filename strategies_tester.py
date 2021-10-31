"""
Este bot actualiza las bases de datos de las estrategias y envía una notificación ante señales de compra y venta.


"""

#Paquetes
from sqlalchemy import create_engine
import os
from funciones.run_saveplot_strategy import run_saveplot_strategy
from datetime import datetime
import strategies
import requests


#Conección a base de datos
engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')

#Limpieza de bbase
engine.execute("DROP TABLE IF EXISTS crypto_strategy_results;")
engine.execute("""CREATE TABLE crypto_strategy_results(market varchar, strategy_name varchar, anual_return numeric); """)

#Parametros a dar en el test
date_today = datetime.today().isoformat()[:10]
ticker = 'BTC-USD'
periodo = 1



#Estrategias
#BOLLRSI
run_saveplot_strategy(strategy= strategies.BOLLRSIStrat, ticker=ticker, strategy_name="BOLLRSI", date=date_today, engine=engine, file_name=f'images/BOLLRSI_BTCUSD.jpg', periodo = periodo)

#emacros100
run_saveplot_strategy(strategy= strategies.emaPriceCross_100, ticker=ticker, strategy_name="EMACross100", date=date_today, engine=engine, file_name=f'images/EMACross100_BTCUSD.jpg')
#emacros150
run_saveplot_strategy(strategy= strategies.emaPriceCross_150, ticker=ticker, strategy_name="EMACross150", date=date_today, engine=engine, file_name=f'images/EMACross150_BTCUSD.jpg')
#emacross200

run_saveplot_strategy(strategy= strategies.emaPriceCross_200, ticker=ticker, strategy_name="EMACross200", date=date_today, engine=engine, file_name=f'images/EMACross200_BTCUSD.jpg')

msg = f"Se actualizaron los datos de las estrategias. También se actualizó la base de datos de Crypto"
mensaje = {'username': 'Adam', 'content': msg}
requests.post(os.environ.get("adam_ema100"), json= mensaje)

