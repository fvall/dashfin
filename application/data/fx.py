import datetime

from ..utils import parse_date
from collections.abc import Iterable
from .providers import DataService


class FX(DataService):

    def __init__(self, *args, **kwargs):
        pass

    currencies = {'USD', 'BRL', 'EUR', 'GBP'}

    def get(self, ccy = None, start = None, end = None, **kwargs):
        
        # ------------
        # Parse dates
        # ------------

        if end is None:
            end = datetime.date.today()

        if start is None:
            start = end
        
        else:
    
            if not isinstance(start, datetime.date):
                try:
                    start = parse_date(start)
                except Exception as e:
                    msg = "\nCannot convert parameter 'start' to date.\n"
                    msg += "------------------------------------------\n"
                    msg += "start : {}".format(str(start))
                    msg += "\n"
                    msg += "Error message: {}".format(str(e))
                    raise ValueError(msg)

            if start > end:
                msg = "Parameter 'start' cannot be greater than 'end'\n"
                msg += "\n-----------------------------------------------\n"
                msg += "start : {}\n"
                msg += "end   : {}"
                msg = msg.format(str(start), str(end))
                raise ValueError(msg)

        if ccy is None:
            ccy = self.currencies
        elif isinstance(ccy, str):
            ccy = [ccy]
        elif not isinstance(ccy, Iterable):
            raise TypeError("ccy must be an iterable")
        else:
            pass
        
        ccy = set(ccy).union(self.currencies)
        for c in ccy:
            if len(c) != 3:
                msg = "Currency must be a string of three characters\n"
                msg += "It is --> {}".format(str(c))
                raise ValueError(msg)
        
        pairs = ['USD' + str(c).upper() + "=X" for c in ccy if c.upper() != 'USD']
        extract = super().get('yahoo')
        
        kwargs = dict(**kwargs)
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['group_by'] = kwargs.get('group_by', 'column')
        quote = extract(pairs, **kwargs)

        quote = quote.loc[:, ['Close']].droplevel(
            0, axis = 1
        ).reset_index().rename(
            columns = dict(Date = 'date')
        ).pipe(
            lambda df: df.rename(
                columns = {
                    c : c[:-2] for c in df.columns if c.endswith("=X")
                }
            )
        )

        return quote
