from botocore.exceptions import ClientError, NoCredentialsError
from pathlib import Path
from sqlalchemy import create_engine
from time import time
from typing import Dict
import pandas as pd
import boto3, glob, logging, os, sys, toml

CONFIG_FILE_NAME = 'config.toml'
OUTPUT_DIRECTORY = 'parquet'
FILE_EXT = '.parquet'
AWS_S3_BUCKET = 'ensembl-genome-data-parquet'

logging.basicConfig(filename="log.txt", level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


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
        logger.error('%s file doesn\'t exist!', config_file_name)
        sys.exit('%s file doesn\'t exist!', config_file_name)
    except Exception as e:
        logger.error(e)
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
                logger.info('Exporting %s table for %s...', table["table_name"], species["species_name"])

                df = pd.read_sql(table['query'], con=engine, params={'species_name': species['species_name']})

                if not os.path.exists(os.path.join(OUTPUT_DIRECTORY, table["table_name"])): os.mkdir(os.path.join(OUTPUT_DIRECTORY, table["table_name"]))

                full_directory_path = os.path.join(OUTPUT_DIRECTORY, table["table_name"], f'species={species["species_name"]}')
                if not os.path.exists(full_directory_path): os.mkdir(full_directory_path)

                file_name = f'{species["db_name"]}-{table["table_name"]}{FILE_EXT}'
                # default engine: pyarrow
                df.to_parquet(os.path.join(full_directory_path, file_name))

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
            file = os.path.relpath(file, os.getcwd())
            # put all the sub directories directly in the S3 bucket, not inside OUTPUT_DIRECTORY folder
            awsPath = file.replace(os.path.join(OUTPUT_DIRECTORY,''), '')
            # for Windows machines convert windows path to UNIX path
            if os.name == 'nt': awsPath = str(Path(awsPath).as_posix())

            try:
                s3_client.upload_file(file, AWS_S3_BUCKET, awsPath)
            except ClientError as e:
                logger.error(e)
            except NoCredentialsError as e:
                logger.error(e)
                sys.exit("ERROR: AWS credentials not found, please refer to readme on how to setup AWS configuration")
            except Exception as e:
                logger.error(e)
                sys.exit(e)

if __name__ == '__main__':
    start = time()

    config = read_config(CONFIG_FILE_NAME)
    logger.info('Exporting SQL data to parquet...')
    try:
        sqlToParquet(config)
    except Exception as e:
        logger.error(e)
        sys.exit(e)

    logger.info('Uploading the parquet files to AWS S3...')
    try:
        uploadDirToS3()
        logger.info('Done, it took a total of %s sec(s).', (time()-start))
    except Exception as e:
        logger.error(e)
