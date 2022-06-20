from sqlalchemy import create_engine
from time import time
import pandas as pd
import toml
import os

start = time()

config = toml.load(open('config.toml'))["config"]

if not os.path.exists('parquet'): os.mkdir('parquet')

for elem in config:
    if (elem["location"] == "local"):
        pass
    else:
        db_connection_str = f'mysql+pymysql://{elem["DB_USER"]}@{elem["location"]}:{elem["port"]}/{elem["species"]}'
        engine = create_engine(db_connection_str)

        for table in elem["data"]["tables"]:
            query = table["query"]
            df = pd.read_sql(query, con=engine, params= [table["vars"]])

            # re-assign column names if duplicate column names exist
            if ("columns" in table.keys()): df.columns = table["columns"].split(", ")

            if not os.path.exists(f'parquet{os.sep}{elem["species"]}'):
                os.mkdir(f'parquet{os.sep}{elem["species"]}')

            # engine: pyarrow
            df.to_parquet(f'parquet{os.sep}{elem["species"]}{os.sep}{table["table"]}.parquet')

print(f'It took {time()-start} secs.')