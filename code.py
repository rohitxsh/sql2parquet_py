from botocore.exceptions import ClientError
from pathlib import Path, PureWindowsPath, PurePosixPath
from sqlalchemy import create_engine
from time import time
from typing import Dict
import pandas as pd
import boto3, glob, logging, os, sys, toml

CONFIG_FILE_NAME = 'config.toml'
OUTPUT_DIRECTORY = 'parquet'
FILE_EXT = '.parquet'
AWS_S3_BUCKET = 'ensembl-genome-data-parquet'

def read_config(config_file_name: str) -> Dict[str, str]:
    '''
    Read TOML file containing the DB info

    Args:
        config_file: TOML configuration file name

    Returns:
        Dictionary containing the parsed data

    Raises:
        FileNotFoundError: If `config_file` doesn't exist
        Exception: Any exception encountered except FileNotFoundError during reading TOML config.
    '''

    try:
        return toml.load(open(config_file_name))
    except FileNotFoundError:
        logging.error(f'"{config_file_name}" file doesn\'t exist!')
        sys.exit(f'"{config_file_name}" file doesn\'t exist!')
    except Exception as e:
        logging.error(e)
        sys.exit(e)

def sqlToParquet(config: Dict[str, str]) -> None:
    '''
    Read tables from remote SQL server and exports the data as parquet files to OUTPUT_DIRECTORY

    Args:
        config: Dictionary config object
    '''

    if not os.path.exists(OUTPUT_DIRECTORY): os.mkdir(OUTPUT_DIRECTORY)

    for database in config['databases']:
        for species in database['species']:

            db_connection_str = f'mysql+pymysql://{database["db_user"]}@{database["location"]}:{database["port"]}/{species["db_name"]}'
            engine = create_engine(db_connection_str)

            for table in database['tables']:
                df = pd.read_sql(table['query'], con=engine, params={'species_name': species['species_name']})

                if not os.path.exists(f'parquet{os.sep}data={table["table_name"]}'): os.mkdir(f'parquet{os.sep}data={table["table_name"]}')

                full_directory_path = f'parquet{os.sep}data={table["table_name"]}{os.sep}species={species["species_name"]}'
                if not os.path.exists(full_directory_path): os.mkdir(full_directory_path)

                # default engine: pyarrow
                df.to_parquet(f'{full_directory_path}{os.sep}{species["db_name"]}-{table["table_name"]}{FILE_EXT}')

def uploadDirToS3() -> None:
    '''
    Uploads all parquet files in OUTPUT_DIRECTORY to AWS_S3_BUCKET

    Raises:
        ClientError: If boto3 faces any errors while uploading the parquet files
    '''

    s3_client = boto3.client('s3')

    for dir in list(Path(OUTPUT_DIRECTORY).glob('**')):
        files = glob.glob(os.path.join(dir, f'*{FILE_EXT}'))

        # skip the iteration if no parquet files in the directory path
        if not files: continue

        for file in files:
            # truncate current working directory path to get relative path
            file = str(file).replace(str(Path.cwd()), '')
            # put all the sub directories directly in the S3 bucket, not inside OUTPUT_DIRECTORY folder
            awsPath = file.replace(f'{OUTPUT_DIRECTORY}{os.sep}', '')
            # for Windows machines convert windows path to UNIX path
            if os.name == 'nt': awsPath = str(PurePosixPath(PureWindowsPath(awsPath)))

            try:
                s3_client.upload_file(file, AWS_S3_BUCKET, awsPath)
            except ClientError as e:
                logging.error(e)

if __name__ == '__main__':
    start = time()

    logging.basicConfig(filename="log.txt", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    config = read_config(CONFIG_FILE_NAME)
    logging.info('Exporting SQL data to parquet...')
    sqlToParquet(config)

    logging.info('Uploading the parquet files to AWS S3...')
    uploadDirToS3()

    logging.info(f'Done, it took a total of {time()-start} secs.')


