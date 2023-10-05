import pandas as pd

from yfinance_portfolio_builder.quote import Quote


class FinancialAsset:
    def __init__(self, ticker, quote, currency):
        self.ticker: str = ticker
        self.last_quote: Quote = quote
        self.currency: str = currency
        self.history: [Quote] = []

    def update_price(self, new_quote: Quote):
        self.history.append(self.last_quote)
        self.last_quote = new_quote

    def populate_quote_history_from_df(self, df_data: pd.DataFrame):
        dates = df_data.index.to_pydatetime().tolist()
        prices = df_data['Close'].tolist()
        self.history = [Quote(date, price) for date, price in zip(dates, prices)]

    def quotes_to_dataframe(self) -> pd.DataFrame:
        data = {
            "Date": [quote.date for quote in self.history],
            "Price": [quote.price for quote in self.history]
        }
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df

    def get_description(self):
        print(f'The ticker for this asset is {self.ticker} and its price is {self.price} {self.currency}')
