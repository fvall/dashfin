import datetime
import pandas as pd

from ...data import FX as fx_data
from itertools import chain, product

from flask import Blueprint, render_template

# --------------------
#  Defining blueprint
# --------------------

fx_bp = Blueprint(
    'fx_bp', __name__,
    template_folder = "templates"
)


def data(ccy = None, start = None, end = None, **kwargs):
    
    service = fx_data()
    quote = service.get(ccy, start = start, end = end, **kwargs)
    quote = quote.sort_values(['date']).fillna(method = "ffill")

    # ------------------
    # Get all ccy pairs
    # ------------------

    pairs = set(chain.from_iterable((c[:3], c[3:]) for c in quote.columns if c != 'date'))
    pairs = ['USD'] + sorted(p for p in pairs if p != 'USD')
    pairs = list(product(pairs, pairs))
    
    for p in pairs:
       
        ticker = p[0] + p[1]
        
        if ticker in quote.columns:
            continue
        
        if p[0] == p[1]:
            quote.insert(len(quote.columns), ticker, 1.0)
        else:

            rate_den = quote.loc[:, "USD" + p[0]]
            rate_num = quote.loc[:, "USD" + p[1]]
            quote.insert(len(quote.columns), ticker, rate_num / rate_den)

    quote = quote.melt(
        id_vars = ['date'],
        var_name = 'fx_pair',
        value_name = 'rate'
    ).assign(
        from_ccy = lambda df: df['fx_pair'].str.slice(0, 3),
        to_ccy   = lambda df: df['fx_pair'].str.slice(3)
    ).drop(columns = ['fx_pair']).query(
        "from_ccy != to_ccy"
    )
    return quote.loc[:, ['date', 'from_ccy', 'to_ccy', 'rate']]


@fx_bp.route('/fx')
def display():
    
    """
    Display FX table
    """

    today = datetime.date.today()
    if today.isoweekday() in (6, 7):
        while today.isoweekday() > 5:
            today -= datetime.timedelta(days = 1)

    fx = data(start = today, end = today)
    ccys = fx['from_ccy'].unique()
    table = pd.DataFrame(index = ccys, columns = ccys)
    for c1 in ccys:
        for c2 in ccys:
            if c1 == c2:
                table.loc[c1, c2] = 1.0
                continue
            table.loc[c1, c2] = fx.loc[
                (fx['from_ccy'] == c1) & (fx['to_ccy'] == c2), 'rate'
            ].iloc[0]
    return render_template('fx-template.html', fx_table = table.to_html())
