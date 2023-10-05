from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

import pandas as pd
import yfinance as yf


class MarketDataDownloadError(Exception):
    """An error raised when there's a problem downloading market data."""

    def __init__(self, cls, method, *args):
        self.cls = cls
        self.method = method
        self.args = args

    def __str__(self):
        return f"Error in class '{self.cls.__name__}', method '{self.method}' with arguments {self.args}"


class YahooFinanceDataLoader:
    @staticmethod
    def get_information_for_ticker(yahoo_ticker) -> yf.Ticker:
        """method to get the information relative to a Yahoo ticker. Raises an exception if ticker doesn't exist."""
        try:
            ticker = yf.Ticker(yahoo_ticker)
            ticker.info
            return ticker
        except Exception:  # This is a general catch-all for exceptions not specified above
            raise MarketDataDownloadError(YahooFinanceDataLoader, 'get_information_for_ticker', yahoo_ticker)

    @staticmethod
    def get_last_close_and_date(ticker_symbol) -> (datetime, float):
        ticker = YahooFinanceDataLoader.get_information_for_ticker(ticker_symbol)
        try:
            hist = ticker.history(period="1d")

            last_date_for_symbol = hist.index[0]
            last_close_for_symbol = hist['Close'][0]

            return last_date_for_symbol, last_close_for_symbol

        except Exception:  # This is a general catch-all for exceptions not specified above
            raise MarketDataDownloadError(YahooFinanceDataLoader, 'get_last_close_and_date', ticker_symbol)

    @staticmethod
    def historical_price(ticker_symbol, start_date=None, end_date=None) -> pd.DataFrame:
        ticker = YahooFinanceDataLoader.get_information_for_ticker(ticker_symbol)
        data = ticker.history(period="1d", start=start_date, end=end_date)
        return data
    
    @staticmethod
    def populate_dataclass(ticker: str, start_date=None, end_date=None):
        try:
            ticker_yahoo = YahooFinanceDataLoader.get_information_for_ticker(ticker)
            info = ticker_yahoo.info
            historical_price = YahooFinanceDataLoader.historical_price(ticker, start_date, end_date)
            return YahooFinanceData(
                ticker=ticker,
                short_name=info.get("shortName"),
                sector=info.get("sector"),
                currency=info.get("currency"),
                market_cap=info.get("marketCap"),
                dividend_yield=info.get("dividendYield"),
                short_ratio=info.get("shortRatio"),
                price_history=historical_price,)
        except Exception:
            raise MarketDataDownloadError(YahooFinanceDataLoader, "populate_dataclass", ticker, start_date, end_date)


@dataclass
class YahooFinanceData:
    ticker: str
    short_name: str
    sector: str
    market_cap: float
    currency: str
    dividend_yield: float
    short_ratio: float
    price_history: pd.DataFrame


if __name__ == "__main__":
    aapl = YahooFinanceDataLoader.populate_dataclass("MSFT")
    print(aapl)