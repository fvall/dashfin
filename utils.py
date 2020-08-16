import re
import datetime


def parse_date(date_):

    if isinstance(date_, datetime.date):
        return date_

    if date_ is None:
        msg = "Cannot convert None to datetime.date object"
        raise ValueError(msg)

    rgx = "[-_/] "
    rgx = re.compile(rgx, re.I)
    dt = rgx.sub('', str(date_))
    try:
        dt = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
    except Exception as e:
        msg = "Cannot convert to datetime.date object\n"
        msg += "Parameter : {}\n"
        msg += "Type      : {}\n"
        msg += "Error message :  {}"
        msg = msg.format(str(date_), type(date_).__name__, str(e))
        raise ValueError(msg)

    return dt
