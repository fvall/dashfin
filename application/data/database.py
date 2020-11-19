import os
import pandas as pd
from .. import config
from ..utils import parse_date

from more_itertools import always_iterable
from sqlalchemy import create_engine


def db_config():
    return os.environ.get('DB')


engine  = create_engine("sqlite:///{}".format(db_config()))


def symbols(*args, **kws):
    return pd.read_sql("SELECT symbol, currency from yahoo_symb", con = engine)


def prices(start = None, end = None, symbols = None):

    if symbols is None:
        symbols = []
    else:
        symbols = list(always_iterable(symbols))

    start = '' if start is None else parse_date(start)
    end   = '' if end is None else parse_date(end)

    # ---------
    #  Filters
    # ---------

    if start != '':
        start = "date >= '{}'".format(start)

    if end != '':
        end = 'date <= "{}"'.format(end)

    symbols = ", ".join("'" + str(s) + "'" for s in symbols)
    if symbols != '':
        symbols = 'symbol in ({})'.format(symbols)

    filters = filter(lambda f: f != '', [start, end, symbols])
    filters = ' AND '.join(filters)

    if filters != '':
        filters = 'WHERE ' + filters

    # -------
    #  Query
    # -------

    query = """
    SELECT *
    from yahoo_price_eod
    {}
    """

    return pd.read_sql(query.format(filters), engine)
