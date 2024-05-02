import argparse
import datetime
import os
import platform
from constants import TerminalColor
import config as cfg
import oracledb
import csv
import logging
import time

def get_config(prm, dml_query,dml_parameters=None):
    oracle_ops = OracleOperations(prm.username, prm.password, prm.tnsname)
    return oracle_ops.execute_query(dml_query, dml_parameters)

def debug(output):
    """Print debug output.

    Parameters
    ----------
    output : Any
        The output to print
    """
    if cfg.debug:
        if isinstance(output, list):
            output = ", ".join(output)
        elif isinstance(output, dict):
            output = ", ".join(str(key) + ": " + str(value) for key, value in output.items())
        print_color(TerminalColor.YELLOW, "DEBUG: {0}: {1}".format(datetime.datetime.now(), output))

def print_color(color, output):
    """Print colored output.

    If $NO_COLOR is set then no colored output will be printed.
    On Windows no colored output will be printed.
    
    Parameters
    ----------
    color : constants.TerminalColor
        The color to be used.
    output : Any
        The output to be printed
    """
    if os.getenv('NO_COLOR') is None and platform.system() != "Windows":
        print(color.value, end='')
        print(output)
        print(TerminalColor.RESET.value, end='')
    else:
        print(output)

def parse_parameter(cmd):
    """Parses the arguments.

    Parameters
    ----------
    cmd : str array
        The arguments passed

    Returns
    -------
    arg
        Argparse object
    """
    parser = argparse.ArgumentParser(
        prog="pyetl2rpt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="The Python ETL 2 Report generator .\nVersion: {0}\n(c) Umesh Rakhe".format(cfg.version)
    )

    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    # Sub Parser generate
    rpt_generate = subparsers.add_parser("generate", aliases=["gen"],
                                            help="Create file based report from SQL statement " +
                                                 "and metadata information from configuration table")
    rpt_generate.add_argument("-i", "--hostname", default="localhost",
                                 help="Metadata server name, default is localhost")
    rpt_generate.add_argument("-n", "--port", default="8889",
                                 help="Metadata server port default is 8889 ")
    rpt_generate.add_argument("-s", "--schema", default='',
                                 help="Metdata server schema")
    rpt_generate.add_argument("-u", "--username", required=True,default="scott",
                                 help="Metdata server UserName default is Scott.")
    rpt_generate.add_argument("-p", "--password",required=True,default="tiger",
                                 help="Metdata server password default is tiger.")
    rpt_generate.add_argument("-t", "--tnsname", default='',
                                 help="tns name to connect metdata server")
    rpt_generate.add_argument("-r", "--retry", default='N',
                                 help="Retry connection if failes")
    rpt_generate.add_argument("-d", "--reportgroup", default='N',
                                 help="Report group to run set of reports")
    rpt_generate.add_argument("-l", "--reportcode", default='N',
                                 help="Report code to run a specific report")
    
    # Sub Parser load
    parser_load = subparsers.add_parser("load", aliases=["lo"],
                                        help="Loads the data from the CSV file(s) into the database.")
    parser_load.add_argument("-i", "--hostname", default="localhost",
                                 help="Metadata server name, default is localhost")
    parser_load.add_argument("-p", "--port", default="8889",
                                 help="Metadata server port default is 8889 ")
    parser_load.add_argument("-s", "--schema", default='',
                                 help="Metdata server schema")
    parser_load.add_argument("-d", "--dbname", default="ORCLPDB1",
                             help="The name of the database.")
    parser_load.add_argument("-u", "--username", required=True,default="scott",
                                 help="Metdata server UserName default is Scott.")
    parser_load.add_argument("-pwd", "--password",required=True,default="tiger",
                                 help="Metdata server password default is tiger.")
    parser_load.add_argument("-t", "--tnsname", default='',
                                 help="tns name to connect metdata server")
    parser_load.add_argument("-r", "--retry", default='N',
                                 help="Retry connection if failes")
    rpt_generate.add_argument("-g", "--loadgroup", default='N',
                                 help="Source File code group to run set of files to load")
    rpt_generate.add_argument("-f", "--srcfilecode", default='N',
                                 help="Source file code to run a specific load")
    
    return parser.parse_args(cmd)

class OracleConnection:
    def __init__(self, username, password, tns_name):
        self.username = username
        self.password = password
        self.tns_name = tns_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = oracledb.connect(
            user=self.username,
            password=self.password,
            dsn=self.tns_name
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.connection.rollback()
            logging.error(f"Error occurred: {exc_value}")
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

class OracleOperations:
    def __init__(self, username, password, tns_name):
        self.username = username
        self.password = password
        self.tns_name = tns_name

    def execute_query(self, query, parameters=None):
        with OracleConnection(self.username,self.password,self.tns_name) as oracle:
            try:
                if parameters:
                    oracle.cursor.execute(query, parameters)
                else:
                    oracle.cursor.execute(query)
                return oracle.cursor.fetchall()
            except oracledb.DatabaseError as e:
                logging.error(f"DatabaseError: {e}")
                raise

    def execute_dml(self, query, parameters=None, max_retries=3, retry_delay=1):
        retries = 0
        while retries < max_retries:
            try:
                with OracleConnection(self.username,self.password,self.tns_name) as oracle:
                    if parameters:
                        oracle.cursor.execute(query, parameters)
                    else:
                        oracle.cursor.execute(query)
                    logging.info("DML operation executed successfully.")
                    return
            except oracledb.DatabaseError as e:
                logging.error(f"DatabaseError: {e}")
                retries += 1
                logging.info(f"Retrying... ({retries}/{max_retries})")
                time.sleep(retry_delay)
        logging.error("Max retries exceeded. Failed to execute DML.")

'''if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(filename='oracle_operations.log', level=logging.DEBUG)

    # Example connection string
    connection_string = "username/password@hostname:port/service_name"

    # Example DDL query
    ddl_query = "CREATE TABLE example_table (id NUMBER PRIMARY KEY, name VARCHAR2(50))"

    # Example DML query
    dml_query = "INSERT INTO example_table (id, name) VALUES (:1, :2)"
    dml_parameters = (1, "Example Name")

    # Example usage
    #oracle_ops = OracleOperations(connection_string)
    #oracle_ops.execute_dml(dml_query, dml_parameters)

    def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = [row for row in reader]
    return data


# Example usage
if __name__ == "__main__":
    # Oracle database connection details
    username = 'your_username'
    password = 'your_password'
    tns_name = 'your_tns_name'  # e.g., 'mytns' from tnsnames.ora

    # File path
    file_path = 'path_to_your_file.csv'

    # Connect to Oracle database and read data from file using context manager
    with OracleDBConnection(username, password, tns_name) as cursor:
        # Perform database operations
        cursor.execute("SELECT * FROM your_table")
        result = cursor.fetchall()
        print("Data from Oracle database:", result)

    # Read data from file using context manager
    file_data = read_data_from_file(file_path)
    print("Data from file:", file_data)
'''