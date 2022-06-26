from pathlib import Path
from sqlalchemy import create_engine
from time import time
import pandas as pd
import os, glob, toml

def sqlToParuet():
    config = toml.load(open('config.toml'))

    if not os.path.exists('parquet'): os.mkdir('parquet')

    for database in config['databases']:
        for species in database['species']:

            db_connection_str = f'mysql+pymysql://{database["DB_USER"]}@{database["location"]}:{database["port"]}/{species["DB_name"]}'
            engine = create_engine(db_connection_str)

            for table in database['tables']:
                df = pd.read_sql(table['query'], con=engine, params={'species_name': species['species_name']})

                directory = f'parquet{os.sep}data={table["table_name"]}{os.sep}species={species["species_name"]}'
                if not os.path.exists('parquet'): os.mkdir('parquet')
                if not os.path.exists(f'parquet{os.sep}data={table["table_name"]}'): os.mkdir(f'parquet{os.sep}data={table["table_name"]}')
                if not os.path.exists(directory): os.mkdir(directory)

                # default engine: pyarrow
                df.to_parquet(f'{directory}{os.sep}{species["DB_name"]}-{table["table_name"]}.parquet')

if __name__ == '__main__':
    start = time()

    sqlToParuet()

    print(f'It took {time()-start} secs.')


