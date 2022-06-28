from sqlalchemy import create_engine
from time import time
import pandas as pd
import os, toml

def read_config(config_file):
    """Read TOML file

    Read TOML file containing the DB info

    Args:
        config_file (str): TOML configuration file name

    Returns:
        Dictionary containing the parsed data.

    Raises:
        FileNotFoundError: If `config_file` doesn't exist.
    """

    try:
        return toml.load(open(config_file))
    except FileNotFoundError:
        print(f'"{config_file}" file does not exist!')
    except Exception as e:
        print(e)

def sqlToParquet(config):
    if not os.path.exists('parquet'): os.mkdir('parquet')

    for database in config['databases']:
        for species in database['species']:

            db_connection_str = f'mysql+pymysql://{database["db_user"]}@{database["location"]}:{database["port"]}/{species["db_name"]}'
            engine = create_engine(db_connection_str)

            for table in database['tables']:
                df = pd.read_sql(table['query'], con=engine, params={'species_name': species['species_name']})

                if not os.path.exists('parquet'): os.mkdir('parquet')
                if not os.path.exists(f'parquet{os.sep}data={table["table_name"]}'): os.mkdir(f'parquet{os.sep}data={table["table_name"]}')

                directory = f'parquet{os.sep}data={table["table_name"]}{os.sep}species={species["species_name"]}'
                if not os.path.exists(directory): os.mkdir(directory)

                # default engine: pyarrow
                df.to_parquet(f'{directory}{os.sep}{species["db_name"]}-{table["table_name"]}.parquet')

if __name__ == '__main__':
    start = time()

    config = read_config('config.toml')
    sqlToParquet(config)

    print(f'It took {time()-start} secs.')


