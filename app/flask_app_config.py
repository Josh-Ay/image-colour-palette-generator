import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Class object that defines the properties/values used to configure the flask application"""
    basedir = os.path.abspath(os.path.dirname(__file__))

    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Class that defines the configuration settings to be used in production"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRE_DATABASE_URL")


class DevelopmentConfig(Config):
    """Class that defines the configuration settings to be used in development"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.basedir + "\\color-extractor-users.db")
