# Python script to move data from SQL to parquet files | GSoC '22

Recommended: Python 3.9.x  
Run the script via  
- `Command line`:
1. Setup your AWS keys as explained here: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#configuration (config. location path: `~/.aws/` [`~` -> Root directory])
2. Run the script via `py -m sql2parquet.sql2parquet`
- `Dockerfile`:
1. Update your AWS keys in `.aws/credentials` [`.aws` directory should be in same directory as the `Dockerfile`]
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

`.aws` configuration files content for reference:

`config`  
[default]  
region=eu-west-2

`credentials`  
[default]  
aws_access_key_id = YOUR_ACCESS_KEY  
aws_secret_access_key = YOUR_SECRET_KEY