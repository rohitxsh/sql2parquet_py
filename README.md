# sql2parquet_py
Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`
Dependency - `map.json`

`map.json` structure:
```
[
    {
        "species": "string, DB name / local file path (if location == 'local')",
        "location": "DB server address / 'local'",
        "port": "DB server's port no.",
        "DB_USER": "username to access the specified DB server, required if location is a DB server address",
        "data": {
            "vars": [
                {
                    "key": "var to be used in sql query for the table, should be a column name returned from the query mentioned below",
                    "query": "query to fetch the above key"
                }
            ],
            "tables": [
                {
                    "table": "table name",
                    "query": "SQL query to construct the table, variables can we used that are defined in vars array by enclosing var.key in curly braces ({}), for ex, if species_id is a var.key then query can we defined as SELECT ... WHERE meta_key={species_id}"
                }
            ]
        }
    }
]
```

Supported DB: MySQL