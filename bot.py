import discord
from sqlalchemy import create_engine, engine
import os
from backtesting_2 import backtester
from asyncio.events import get_event_loop
import discord

engine = create_engine(f'postgresql://{os.environ.get("db_user")}:{os.environ.get("db_pass")}@{os.environ.get("db_host")}/tablero_acciones')


backtester()


