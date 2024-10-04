import os
from dotenv import load_dotenv
from pathlib import Path

import sqlalchemy
import psycopg2
import asyncpg
import pandas as pd
import datetime as dt

from structure import struct

#путь к файлу с данными для входа
dotenv_path = Path(rf'.\.env')
load_dotenv(dotenv_path=dotenv_path)


engine = sqlalchemy.create_engine(os.getenv('engine', 'default') % os.getenv('dp_port', 'default'))
autocommit_engine = engine.execution_options(isolation_level="AUTOCOMMIT")


def server(flag: bool):

    params = {
        'database': os.getenv('db_name', 'default'),
        'user': os.getenv('db_un', 'default'),
        'password': 'aboba54!',#os.getenv('db_pw', 'default'),
        'host': os.getenv('host', 'default'),
        'port': os.getenv('dp_port', 'default')
    }
    
    connection = psycopg2.connect(**params)
    cursor = connection.cursor()

    connection.autocommit = True

    if flag:
        return connection
    else:
        return cursor
    

con = server(True)
cur = server(False)

cur.execute(struct)
con.commit()


async def check_mnemonic_async(mnemonics: list, pool):
    async with pool.acquire() as connection:
        query = f"SELECT * FROM ton.wallet WHERE mnemonic = $1"
        result = await connection.fetch(query, ' '.join(mnemonics))
        return len(result) == 0


async def add_data_async(b, w, m, pool):
    async with pool.acquire() as connection:
        query = f"INSERT INTO ton.wallet (balance, wallet_address, mnemonic) VALUES ($1, $2, $3)"
        await connection.execute(query, b, w, ' '.join(m))


def check_mnemonic(mnemonics: list) -> bool:
    return pd.read_sql(f''' select * from ton.wallet where mnemonic='{" ".join(mnemonics)}' ''', con).empty


def add_data(b, w, m) -> None:
    cur.execute(fr''' INSERT INTO ton.wallet VALUES ({b}, '{w}', '{' '.join(m)}') ''')
    con.commit()
