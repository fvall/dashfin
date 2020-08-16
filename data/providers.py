import yfinance as yf


class Yahoo(object):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def get(*args, **kwargs):
        return yf.download(*args, **kwargs)


class DataService(object):

    def __init__(self, *args, **kwargs):
        pass

    clients = dict(
        yahoo = Yahoo()
    )

    @classmethod
    def get(cls, provider):
        
        client = cls.clients.get(str(provider).lower())
        if client is None:
            msg = "Cannot extract data from this provider.\n"
            msg += "Provider : {}\n".format(str(provider))
            msg += "List of providers : {}".format(", ".join(cls.clients))
            raise ValueError(msg)

        def extract(*args, **kwargs):
            return client.get(*args, **kwargs)
        
        return extract
