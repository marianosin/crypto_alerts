
from sqlalchemy import create_engine
import os
from funciones.run_saveplot_strategy import run_saveplot_strategy
import requests
import discord
import strategies

engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')
engine.execute("DROP TABLE IF EXISTS crypto_strategy_results;")
engine.execute("""CREATE TABLE crypto_strategy_results(market varchar, strategy_name varchar, anual_return numeric); """)


date_today = '2021-10-22'
ticker = 'BTC-USD'
#BOLLRSI
run_saveplot_strategy(strategy= strategies.BOLLRSIStrat, ticker=ticker, strategy_name="BOLLRSI", date=date_today, engine=engine, file_name=f'images/BOLLRSI_BTCUSD.jpg')

#emacros100
run_saveplot_strategy(strategy= strategies.emaPriceCross_100, ticker=ticker, strategy_name="EMACross100", date=date_today, engine=engine, file_name=f'images/EMACross100_BTCUSD.jpg')
#emacros150
run_saveplot_strategy(strategy= strategies.emaPriceCross_150, ticker=ticker, strategy_name="EMACross150", date=date_today, engine=engine, file_name=f'images/EMACross150_BTCUSD.jpg')
#emacross200

run_saveplot_strategy(strategy= strategies.emaPriceCross_200, ticker=ticker, strategy_name="EMACross200", date=date_today, engine=engine, file_name=f'images/EMACross200_BTCUSD.jpg')



#Sistema de notificaciones



mensaje = {'username': 'Adam', 'content': "Hola"}

requests.post(os.environ.get("adam_ema100"), json= mensaje)


