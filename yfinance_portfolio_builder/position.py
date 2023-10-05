from datetime import datetime

from yfinance_portfolio_builder.financial_asset import FinancialAsset


class Position:
    def __init__(self, financial_asset: FinancialAsset, weight: float = 0, quantity: float = 0):
        self.financial_asset = financial_asset
        self.weight = weight
        self.quantity = quantity
        self.historical_weight: dict = {}
        self.historical_quantity: dict = {}

    def update_weight(self, weight: float, update_date: datetime = None):
        if datetime is None:
            update_date = datetime.now()
        self.historical_weight[update_date] = self.weight
        self.weight = weight

    def update_quantity(self, quantity: float, update_date: datetime = None):
        if update_date is None:
            update_date = datetime.now()
        self.historical_quantity[update_date] = self.quantity
        self.quantity = quantity

