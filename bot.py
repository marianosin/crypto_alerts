from backtrader import strategy
import discord
from sqlalchemy import create_engine
import os
from funciones.run_saveplot_strategy import run_saveplot_strategy

import discord
import strategies

engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')
engine.execute("DROP TABLE IF EXISTS crypto_strategy_results;")
engine.execute("""CREATE TABLE crypto_strategy_results(market varchar, strategy_name varchar, anual_return numeric); """)

run_saveplot_strategy(strategy= strategies.BOLLRSIStrat, ticker="BTC-USD", strategy_name="BOLLRSI", date='2021-10-20', engine=engine, file_name='images/BOLLRSI_BTCUSD.jpg')
