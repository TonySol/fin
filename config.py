"""Configuration is aggregated here

os.environ.get – gets from .env by dict key
Running the flask command will set environment variables defined in the files .env and .flaskenv
Thus we don't need to explicitly import and call load_dotenv()
"""
import os

from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
server = os.environ.get('DB_SERVER')
database = os.environ.get('DB_DATABASE')


class Config:
    """Basic config class for production"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{server}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Config):
    """Dev config with public server on"""
    DEBUG = True
    SERVER_NAME = "192.168.0.185:5000"


class Test(Config):
    """Test config with sqllite db"""
    TESTING = True
    SECRET_KEY = "test-key"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
