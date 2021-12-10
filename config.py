"""Configuration is aggregated here

os.environ.get – gets from .env by dict key
Running the flask command will set environment variables defined in the files .env and .flaskenv
Thus we don't need to explicitly import and call load_dotenv()
"""
import os


# from dotenv import load_dotenv
# load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = False

class Development(Config):
    DEBUG = True
    SERVER_NAME = "192.168.0.185:5000"
