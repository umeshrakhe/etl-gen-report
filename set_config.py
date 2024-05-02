
from dotenv import load_dotenv
import os

def get_env_variables():
    print("sample method")


def load_env_variables(self):
        env_file = f".env.{self.context}"
        load_dotenv(env_file)

        self.db_type = os.getenv("DB_TYPE")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

def setup_logger(self):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger