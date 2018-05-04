import csv
import requests

from . import db
from .models import Tickers

__author__ = 'mukundmk'


def quandle_codes_helper():
    db.drop_all()

    resp = requests.get('http://static.quandl.com/end_of_day_us_stocks/ticker_list.csv')
    if resp.status_code != 200:
        return False

    db.create_all()

    data = resp.content.decode('utf-8')
    csv_data = csv.reader(data.splitlines(), delimiter=',')

    for row in csv_data:

        ticker_obj = Tickers(ticker=row[0], name=row[2])
        db.session.add(ticker_obj)

    db.session.commit()
    return True
