import quandl
import quandl.errors.quandl_error
import datetime

from flask import request, render_template, jsonify

from . import app
from .models import Tickers

__author__ = 'mukundmk'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_prices')
def get_prices():
    response = {'dates': ['dates'], 'prices': ['prices'], 'averages': ['averages']}
    avg_num = 0.0
    today = datetime.date.today()
    duration = request.args.get('duration', 'max')
    try:
        if duration == 'max':
            prices = quandl.get('EOD/{}'.format(request.args.get('ticker', 'AAPL')), returns='numpy',
                                column_index=request.args.get('column', 4), collapse='quarterly')

        elif duration == '5year':
            start = today.replace(year=today.year - 5)
            prices = quandl.get('EOD/{}'.format(request.args.get('ticker', 'AAPL')), returns='numpy',
                                start_date=start.strftime('%Y-%m-%d'), column_index=request.args.get('column', 4),
                                collapse='monthly')

        elif duration == 'year':
            start = today.replace(year=today.year - 1)
            prices = quandl.get('EOD/{}'.format(request.args.get('ticker', 'AAPL')), returns='numpy',
                                start_date=start.strftime('%Y-%m-%d'), column_index=request.args.get('column', 4),
                                collapse='weekly')

        else:
            start = (today.replace(day=1) - datetime.timedelta(1)).replace(day=today.day)
            prices = quandl.get('EOD/{}'.format(request.args.get('ticker', 'AAPL')), returns='numpy',
                                start_date=start.strftime('%Y-%m-%d'), column_index=request.args.get('column', 4))

    except quandl.errors.quandl_error.ForbiddenError:
        return '', 403

    for i, (date, price) in enumerate(prices):
        response['dates'].append(date.strftime('%Y-%m-%d'))
        response['prices'].append(price)

        if i < 5:
            avg_num += price
            response['averages'].append(avg_num / (i + 1))

        else:
            avg_num += price - prices[i - 5][1]
            response['averages'].append(avg_num / 5)

    return jsonify(response)


@app.route('/autocomplete')
def autocomplete():
    response = {'suggestions': []}
    matches = Tickers.query.filter(Tickers.name.ilike('{}%'.format(request.args.get('query', '')))).limit(3).all()

    for match in matches:
        response['suggestions'].append({'value': match.name, 'ticker': match.ticker})

    return jsonify(response)
