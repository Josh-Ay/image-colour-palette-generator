import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Class object that defines the properties/values used to configure the flask application"""
    basedir = os.path.abspath(os.path.dirname(__file__))

    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProductionConfig(Config):
    """Class that defines the configuration settings to be used in production"""
    pass



class DevelopmentConfig(Config):
    """Class that defines the configuration settings to be used in development"""
    pass
