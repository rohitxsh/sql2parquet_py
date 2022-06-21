# Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`  
Dependency - `config.toml`

`config.toml`
```
[[config]]
species = "string, DB name / local file path (if location == 'local')"
location = "string, DB server address / 'local'"
port = "string, DB server's port no."
DB_USER = "string, username to access the specified DB server, required if location is a DB server address"
[[config.data.tables]]
table = "string, table name"
query = '''
milti-line string, SQL query to construct the table, variables can we used that are defined in vars array
'''
columns = "string with column names separated by commas, needed if columns names need to be renamed in the new table"
vars = ["string"], params to be used in the query
```

Supported DB: MySQL
