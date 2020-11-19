import numpy as np
import pandas as pd
import datetime

import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns

from flask import (
    Blueprint, render_template,
    session, jsonify, make_response,
    current_app
)

from ...data.database import prices, symbols


home_bp = Blueprint("home_bp", __name__, template_folder = "templates")
matplotlib.use('Agg')


def random_table():
    
    headers = ['a', 'b', 'c']
    values  = [100, 200, 300, 400, 500]
    tbl = pd.DataFrame({
        k : values for k in headers
    })
    return tbl


def ts_chart(tbl):

    plot_output = BytesIO()
    plt.figure(figsize=[12, 6])

    # x = np.arange(0, 100, 0.001)
    # tbl = random.randint(1, 10)
    # y = x * np.sin(tbl * np.pi * x)

    output = []
    for _, gp in tbl.groupby(['symbol']):
        output.append(
            gp
            .sort_values(['date'])
            .assign(
                ret = lambda df: df['price'] / df['price'].iloc[0] - 1.0
            )
        )

    output = pd.concat(output, sort = False)
    plot = sns.lineplot(
        x = 'date',
        y = 'ret',
        hue  = 'symbol',
        data = output
    )
    # plt.axis('off')
    plot.get_figure().savefig(plot_output, format = 'svg')
    return plot_output.getvalue().decode('utf-8')


@home_bp.route("/symbol/<string:symb>", methods = ['POST'])
def update_symbol(symb):
    session['symbol'] = symb.split(',')
    return jsonify(symb)


def get_symbol():
    if 'symbol' not in session:
        session['symbol'] = ''
    
    return session["symbol"]


@home_bp.route('/chart')
def chart():

    tbl = prices(
        session['start'], session['end'],
        symbols = session.get('symbol')
    )[[
        'symbol', 'adj_close', 'date', 'volume'
    ]].rename(
        columns = {'adj_close' : 'price'}
    )

    response = make_response(ts_chart(tbl))
    response.mimetype = 'image/svg+xml'
    return response


@home_bp.route("/")
@home_bp.route("/home")
def home():

    llist = sorted(symbols()['symbol'].unique())
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days = 365)
    start = start.date()
    end   = now.date()

    session['start'] = str(start)
    session['end'] = str(end)

    idx_tbl = random_table().to_html(index = False)
    fx_tbl = random_table().to_html(index = False)
    return render_template(
        "home.html", idx_tbl = idx_tbl, fx_tbl = fx_tbl,
        options = llist
    )
