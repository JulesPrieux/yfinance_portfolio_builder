"""
**Exercise 6: Implementing a Modified Equity Portfolio Strategy**

**Objective**: Design a new strategy named `EqualWeightShortRatioAdjusted` for the `EquityPortfolio` and create a 
portfolio which implements it

**Steps**:

1. **Set up the DataLoader**:
   - Navigate to the `resources.DataLoader.py` file.
   - Copy and paste the implementation of the `YahooFinanceDataLoader` class (which was modified in the previous 
   exercise) into this file.

2. **Update the Equity Class**:
   - Amend the `Equity` class to incorporate new attributes that align with those present in the 
   `YahooFinanceDataLoader` (e.g., `ticker`, `shortName`, `sector`, etc.).

3. **Construct the New Strategy**:
   - In the `resources.Strategies.py` file, define a new strategy named `EqualWeightShortRatioAdjusted`.
   - Implement the strategy with the following logic:
     - Start with an equal weight strategy across all equities.
     - Adjust the weights based on the `short_ratio`:
       - Identify the three stocks with the highest short ratio in the universe. Halve their weights.
       - Boost the weights of the three stocks with the lowest short ratio in the universe by the amount subtracted 
       from the most shorted stocks.

4. **Implement the Strategy in the Portfolio**:
   - Instantiate an `EquityPortfolio` object (e.g., `equityPft`) and apply the `EqualWeightShortRatioAdjusted` 
   strategy to it.
   - Rebalance the portfolio using the aforementioned strategy.
   - For this exercise, ensure the following stocks are included in the universe:
     - `MMM`
     - `ABBV`
     - `ATVI`
     - `BIO`
     - `CPB`
     - `COF`
     - `CF`
     - `SCHW`
     - `CHTR`
     - `LLY`
"""