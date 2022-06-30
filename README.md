# Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`  
Dependency - `config.toml`

`config.toml` schema:
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

Refer to https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration  
for AWS boto3 configuration setup

AWS boto3 configuration used (for reference)
### `config`
[default]  
region=eu-west-2

### `credentials`
[default]  
aws_access_key_id = YOUR_ACCESS_KEY  
aws_secret_access_key = YOUR_SECRET_KEY