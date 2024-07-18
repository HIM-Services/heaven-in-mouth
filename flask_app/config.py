import os
from dotenv import load_dotenv


# read database credentials from enviroment
def get_env_variable(name):
    try:
        return os.getenv(name)
    except KeyError:
        message = f"Expected environment variable '{name}' not set."
        raise Exception(message)


# dotenv is used to read the .env file and set the environment variables
load_dotenv()


class Config:
    SECRET_KEY = get_env_variable("SECRET_KEY")
    SESSION_TYPE = 'filesystem'
    # Set in docker
    # SESSION_TYPE = get_env_variable("SESSION_TYPE")

    POSTGRES_URL = get_env_variable("POSTGRES_URL")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_PW = get_env_variable("POSTGRES_PW")
    POSTGRES_DB = get_env_variable("POSTGRES_DB")

    DB_URL = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}/{POSTGRES_DB}'

    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
