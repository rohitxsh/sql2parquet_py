# Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`
Dependency - `config.toml`

`config.toml`
```
[[databases]]
location = "string, DB server address"
port="string, DB server's port no."
DB_USER="string, username to access the specified DB server"
[[databases.species]]
DBname="string, DB name"
species="string, species scientific name"
[[databases.tables]]
table = "string, table name"
query = '''
milti-line string, SQL query to construct the table, variables can we used that are defined in vars
'''
```

Supported DB: MySQL
Engine: PyMySQL
