from flask import Flask
from dotenv import load_dotenv
import os
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_compress import Compress

load_dotenv()  # load the variables stored in the .env file

# initialising a database and oauth object handlers
client = MongoClient(os.environ.get("MONGO_DB_URI"))
oauth = OAuth()

# initialising a gzip compression object
compress = Compress()

# registering an oauth client for google
oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    client_kwargs={'scope': 'email profile'},
)

# registering an oauth client for github
oauth.register(
    name='github',
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user email'},
)


def get_db():
    return client.colorsDB


def configure_app(app):
    oauth.init_app(app)
    compress.init_app(app)


def create_flask_app(config):
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    app.config.from_object(config)

    Bootstrap(app)
    configure_app(app)

    return app
