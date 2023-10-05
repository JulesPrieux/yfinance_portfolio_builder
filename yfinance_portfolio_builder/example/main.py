"""Example use."""
from uuid import uuid4
from threading import Thread

from yfinance_portfolio_builder.portfolio import Equity, EquityPft
from yfinance_portfolio_builder.strategies import EqualWeightShortRatioAdjusted


TICKERS = ["ABBV", "ATVI", "BIO", "CPB", "COF", "CF", "SCHW", "CHTR", "LLY"]

def populate_list(ticker: str, instruments: list):
    equity = Equity.from_ticker(ticker)
    instruments.append(equity)

if __name__ == '__main__':
    threads, instruments = [], []
    for ticker in TICKERS:
        t = Thread(target=populate_list, args=(ticker, instruments))
        threads.append(t)
        t.start()

    [thread.join() for thread in threads]

    pft = EquityPft("Short ratios",
                    uuid4(),
                    "USD",
                    1_000_000,
                    100,
                    EqualWeightShortRatioAdjusted,)
    pft.initialize_position_from_instrument_list(instruments)
    pft.rebalance_portfolio()
    print(pft.portfolio_position_summary())
