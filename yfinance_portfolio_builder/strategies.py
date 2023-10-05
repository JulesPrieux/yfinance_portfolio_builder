import heapq
from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def generate_signals(self, data_for_signal_generation: dict):
        """
        Generate trading signals based on a series of prices.

        Parameters:
        - data_for_signal_generation: A dictionary with tickers as keys and positions as values.

        Returns:
        - A dictionary with tickers as keys and signals as values.
        """
        pass


class EqualWeightStrategy(Strategy):

    @staticmethod
    def generate_signals(position_dict: dict):
        tickers = position_dict.keys()
        equal_weight = 1 / len(tickers)
        return {ticker: equal_weight for ticker in tickers}


class EqualWeightShortRatioAdjusted(Strategy):

    @staticmethod
    def get_top_bot_shorted_assets(position_dict: dict, x: int) -> tuple[list]:
        """Return the top & bot shorted assets.

        Args:
            position_dict (dict): A dictionary with tickers as keys and positions as values.
            x (int, optional): The number of stocks to return. Defaults to 3.

        Returns:
            list: the x top shorted stocks, x least shorted stocks.
        """
        if x > len(position_dict):
            raise ValueError("x is larger than the lenght of the dictionnary.")
        short_ratios = {ticker: position.financial_asset.short_ratio \
                        for ticker, position in position_dict.items()}
        descending_short_ratios = sorted(short_ratios.items(), key=lambda x:x[1], reverse=True)
        descending_tickers = [ticker for (ticker, ratio) in descending_short_ratios]
        return descending_tickers[:3], descending_tickers[-3:]

    @staticmethod
    def generate_signals(position_dict: dict, x: int = 3):
        top_shorted, bot_shorted = EqualWeightShortRatioAdjusted.get_top_bot_shorted_assets(position_dict, x)
        equal_weight = EqualWeightStrategy.generate_signals(position_dict)
        for top, bot in zip(top_shorted, bot_shorted):
            equal_weight[top] /= 2
            equal_weight[bot] += equal_weight[bot] / 2
        return equal_weight
        


