# Python script to move data from SQL to parquet files | GSoC '22

Requires Python 3.x  
Run the script via  
- Cmd. line: `py -m sql2parquet.sql2parquet`
- `Dockerfile`:
1. Update your AWS keys in `.aws/credentials`
2. Build the image from the dockerfile via `docker build --tag sql2parquet .`
3. Run the container via `docker run sql2parquet`

---

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

---

Refer to https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration  
for AWS boto3 configuration setup

### `config`
[default]  
region=eu-west-2

### `credentials`
[default]  
aws_access_key_id = YOUR_ACCESS_KEY  
aws_secret_access_key = YOUR_SECRET_KEY
