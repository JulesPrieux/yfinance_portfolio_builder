import math
from datetime import datetime

import pandas as pd

# import ressources.Strategies as Strategy
from yfinance_portfolio_builder.strategies import Strategy
from yfinance_portfolio_builder.financial_asset import FinancialAsset
from yfinance_portfolio_builder.position import Position
from yfinance_portfolio_builder.data_loader import YahooFinanceDataLoader, YahooFinanceData
from yfinance_portfolio_builder.quote import Quote
# from ressources.StrategiesV2 import Strategy


class Equity(FinancialAsset):
    def __init__(self, ticker, last_quote, currency, short_name, sector, market_cap, dividend_yield, short_ratio):
        super().__init__(ticker, last_quote, currency)
        self.short_name = short_name
        self.sector = sector
        self.market_cap = market_cap
        self.dividend_yield = dividend_yield
        self.short_ratio = short_ratio

    @staticmethod
    def from_ticker(ticker: str):
        data = YahooFinanceDataLoader.populate_dataclass(ticker)
        last_quote = Quote(*YahooFinanceDataLoader.get_last_close_and_date(ticker))
        equity = Equity(
            ticker=data.ticker,
            last_quote=last_quote,
            currency=data.currency,
            short_name=data.short_name,
            sector=data.sector,
            market_cap=data.market_cap,
            dividend_yield=data.dividend_yield,
            short_ratio=data.short_ratio,)
        equity.populate_quote_history_from_df(data.price_history)
        return equity
        
    def __str__(self) -> str:
        return (f'The ticker for this asset is {self.ticker} and its price is {self.last_quote.price} {self.currency}.'
              f' Last dividend was {self.dividend_yield}')
    
    def __repr__(self) -> str:
        attrs = vars(self)
        return ", ".join((f"{k}={v}" for k, v in attrs.items()))



class EquityPft:
    def __init__(self, name, code, currency, aum, nb_of_shares, strategy: Strategy):
        self.name: str = name
        self.code: str = code
        self.currency: str = currency
        self.aum: float = aum
        self.nb_of_shares: float = nb_of_shares
        self.historical_NAV: [float] = []
        self.positions: [Position] = []
        self.strategy = strategy

    def _positions_to_dict(self):
        return {position.financial_asset.ticker: position for position in self.positions if position.weight is not None}

    def initialize_position_from_instrument_list(self, instrument_list: [FinancialAsset]):
        for instrument in instrument_list:
            instrument_position = Position(instrument)
            self.positions.append(instrument_position)
        

    def rebalance_portfolio(self, rebalancing_date: datetime = datetime.now()):
        # position_dict = self._positions_to_dict()
        # weights = self.strategy.generate_signals(position_dict, 2)
        # self.positions = []
        # for ticker, weight in weights.items():
        #     self.
        positions_dict = self._positions_to_dict()
        signals = self.strategy.generate_signals(positions_dict)

        for position in self.positions:
            ticker = position.financial_asset.ticker
            weight = signals.get(ticker, 0)
            new_quantity = math.floor((self.aum * weight) / position.financial_asset.last_quote.price)
            position.update_quantity(new_quantity, rebalancing_date)
            position.update_weight(weight, rebalancing_date)

    def portfolio_position_summary(self) -> pd.DataFrame:
        tickers = [position.financial_asset.ticker for position in self.positions]
        weights = [position.weight for position in self.positions]
        quantities = [position.quantity for position in self.positions]
        last_prices = [position.financial_asset.last_quote.price for position in self.positions]

        data = {
            "Ticker": tickers,
            "Weight": weights,
            "Quantity": quantities,
            "Last close": last_prices
        }
        return pd.DataFrame(data)
