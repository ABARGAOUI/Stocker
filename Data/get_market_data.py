import requests_cache
import yfinance as yf


class CachedYahooMarketData:

    def __init__(self, session_name, tickers, start_date):
        self.session = requests_cache.CachedSession("{}_yfinance.cache".format(session_name))
        self.session.headers['User-agent'] = 'my-program/1.0'
        #self.tickers = yf.Tickers(tickers, session=self.session)
        #self.tickers.download(start_date=start_date)



