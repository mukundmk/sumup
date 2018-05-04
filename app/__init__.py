import quandl

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

__author__ = 'mukundmk'


app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

quandl.ApiConfig.api_key = app.config['QUANDL_API_KEY']

from . import views, models