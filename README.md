# Python script to move data from SQL to parquet files | GSoC '22

The python script - `code.py`  
Dependency - `map.json`

`map.json`
```
[
    {
        "species": "string, DB name / local file path (if location == 'local')",
        "location": "string, DB server address / 'local'",
        "port": "string, DB server's port no.",
        "DB_USER": "string, username to access the specified DB server, required if location is a DB server address",
        "data": {
            "vars": [
                {
                    "key": "string, var to be used in sql query for the table, should be a column name returned from the query mentioned below",
                    "query": "string, query to fetch the above key"
                }
            ],
            "tables": [
                {
                    "table": "string, table name",
                    "query": "string, SQL query to construct the table, variables can we used that are defined in vars array by enclosing var.key in curly braces ({}), for ex, if species_id is a var.key then query can we defined as SELECT ... WHERE meta_key={species_id}, seperate multiline queries via \r\n"
                }
            ]
        }
    }
]
```

Supported DB: MySQL
