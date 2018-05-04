from . import db

__author__ = 'mukundmk'


class Tickers(db.Model):
    ticker = db.Column(db.String(12), primary_key=True)
    name = db.Column(db.String(256))
