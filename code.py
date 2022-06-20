from sqlalchemy import create_engine
import pandas as pd
import toml
import os

config = toml.load(open('config.toml'))["config"]

for elem in config:
    if (elem["location"] == "local"):
        pass
    else:
        db_connection_str = f'mysql+pymysql://{elem["DB_USER"]}@{elem["location"]}:{elem["port"]}/{elem["species"]}'
        engine = create_engine(db_connection_str)

        queryVars = {}
        for i in elem["data"]["vars"]:
            queryVars[i["key"]] = pd.read_sql(i["query"], con=engine)[i["key"]].item()

        for table in elem["data"]["tables"]:
            query = table["query"]
            for queryVar in queryVars:
                if ("{"+queryVar+"}" in query): query = query.replace("{"+queryVar+"}", str(queryVars[queryVar]))
            df = pd.read_sql(query, con=engine)

            # re-assign column names if duplicate column names exist
            if ("columns" in table.keys()): df.columns = table["columns"].split(", ")

            if not os.path.exists(f'parquet{os.sep}{elem["species"]}'):
                os.mkdir(f'parquet{os.sep}{elem["species"]}')

            # engine: pyarrow
            df.to_parquet(f'parquet{os.sep}{elem["species"]}{os.sep}{table["table"]}.parquet')
