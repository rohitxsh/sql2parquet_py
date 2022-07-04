FROM python:3.9

COPY sql2parquet/__init__.py /sql2parquet/__init__.py
COPY sql2parquet/sql2parquet.py /sql2parquet/sql2parquet.py

COPY config.toml config.toml
COPY .aws /root/.aws

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "sql2parquet.sql2parquet"]