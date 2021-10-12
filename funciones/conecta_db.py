import psycopg2
import os

def conecta_db(dbname, user = os.environ.get('db_user'), password = os.environ.get('db_pass'), host = os.environ.get('db_host')):
    conn = psycopg2.connect(dbname = dbname, 
                        user = user,
                        password = password,
                        host = host)
    return conn