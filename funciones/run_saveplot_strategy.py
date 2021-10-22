
import strategies
from funciones.run_backtest import runstrat
from funciones.save_backtrader_plot import saveplots

stname = ["RSI","BOLL", "BOLLRSI","EMACROSS","SMAsCROSS", "SMACROSS"]
markets = ["BTC-USD", "ADA-USD","ETH-USD", "LTC-USD", "BNB-USD"]


def run_saveplot_strategy(strategy, ticker, strategy_name, date, engine, file_name,periodo = 1):
    """Corre la función para guardar los graficos que se enviarán por mensaje

    Args:
        strategy (class): Define la estrategia
        ticker (str): Define el ticker a correr
        strategy_name (str): Hay que darle un nombre para guardar en la base de datos
        date (date): Fecha última para calcular.
        engine (sql): Conección a sql
        file_name (str): Nombre del archivo para ser guardado
        periodo (int, optional): Define el periodo de operación para bajar los datos. Defaults to 1.
    """

    saveplots(runstrat(strategy, strategy_name=strategy_name, date= date, engine= engine, ticker= ticker, periodo= periodo),file_path=file_name)

