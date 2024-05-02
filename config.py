
#import psycopg2
#import pymysql
import sqlite3
from contextlib import contextmanager

version="1.0.1"
debug=True
load_confi_sql='select * from configuration where src_file_cd='
rpt_config_sql="select * from generate_rpt where src_file_cd="

from time import sleep



'''class DatabaseConnector:
    def __init__(self, context='development'):
        self.context = context
        self.load_env_variables()
        self.logger = self.setup_logger()

    def connect_with_retry(self, max_retries=3, retry_delay=3):
        retries = 0
        while retries < max_retries:
            try:
                return self.connect()
            except Exception as e:
                self.logger.error(f"Connection failed: {e}")
                retries += 1
                if retries < max_retries:
                    self.logger.info(f"Retrying connection after {retry_delay} seconds...")
                    sleep(retry_delay)
                else:
                    raise

    def connect(self):
        if self.db_type == 'postgresql':
            return self.connect_postgresql()
        elif self.db_type == 'mysql':
            return self.connect_mysql()
        elif self.db_type == 'sqlite':
            return self.connect_sqlite()
        else:
            self.logger.error("Unsupported database type.")
            return None

    def connect_postgresql(self):
        try:
            connection = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            self.logger.info("PostgreSQL Database connected successfully!")
            return connection
        except psycopg2.Error as e:
            self.logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise

    def connect_mysql(self):
        try:
            connection = pymysql.connect(
                host=self.db_host,
                port=int(self.db_port),
                database=self.db_name,
                user=self.db_user,
                password=self.db_password
            )
            self.logger.info("MySQL Database connected successfully!")
            return connection
        except pymysql.Error as e:
            self.logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def connect_sqlite(self):
        try:
            connection = sqlite3.connect(self.db_name)
            self.logger.info("SQLite Database connected successfully!")
            return connection
        except sqlite3.Error as e:
            self.logger.error(f"Error connecting to SQLite database: {e}")
            raise

# Example usage:
# Initialize the DatabaseConnector with context 'production'
db_connector = DatabaseConnector(context='production')

# Connect to the database with retry
connection = db_connector.connect_with_retry(max_retries=3, retry_delay=3)
'''