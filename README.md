# Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`  
Dependency - `config.toml`

`config.toml`
```
[[config]]
species = "string, DB name"
location = "string, DB server address"
port = "string, DB server's port no."
DB_USER = "string, username to access the specified DB server"
[[config.data.tables]]
table = "string, table name"
query = '''
milti-line string, SQL query to construct the table, variables can we used that are defined in vars
'''
[config.data.tables.vars]
var_key = "string, var_value"
```

Supported DB: MySQL
