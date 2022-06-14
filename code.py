from sqlalchemy import create_engine, inspect
import pandas as pd
import os

DB_URL = "ensembldb.ensembl.org:3306"
DB_NAME = "homo_sapiens_core_106_38"
DB_USER = "anonymous"

db_connection_str = 'mysql+pymysql://anonymous@ensembldb.ensembl.org:3306/homo_sapiens_core_106_38'
engine = create_engine(db_connection_str)
inspector = inspect(engine)

tables = inspector.get_table_names()

# for table in tables:
#     df = pd.read_sql(f'select * FROM {table}', con=engine)

df = pd.read_sql(f'select * FROM {tables[0]}', con=engine)

if not os.path.exists(f'parquet{os.sep}{DB_NAME}'):
    os.mkdir(f'parquet{os.sep}{DB_NAME}')

# engine: pyarrow
df.to_parquet(f'parquet{os.sep}{DB_NAME}{os.sep}{tables[0]}.parquet')