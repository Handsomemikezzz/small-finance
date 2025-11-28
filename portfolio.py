class Portfolio:
    def __init__(self, initial_capital, position_size_pct=1.0, stop_loss_pct=None, take_profit_pct=None):
        """
        Initializes the portfolio.

        Args:
            initial_capital (float): Starting cash.
            position_size_pct (float): Percentage of portfolio to allocate to the trade (0.0 to 1.0).
            stop_loss_pct (float): Stop loss percentage (e.g., 0.05 for 5%). None to disable.
            take_profit_pct (float): Take profit percentage (e.g., 0.10 for 10%). None to disable.
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.holdings = 0
        self.total_value = initial_capital
        self.position_size_pct = position_size_pct
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct

        # Track trade entry price for SL/TP
        self.entry_price = 0

        self.history = [] # To store portfolio value over time
        self.trades = []  # To store trade details

    def update_value(self, current_price, date):
        """Updates the total portfolio value based on current price."""
        market_value = self.holdings * current_price
        self.total_value = self.cash + market_value
        self.history.append({'Date': date, 'Total Value': self.total_value})

    def check_risk_management(self, current_price, date):
        """
        Checks for stop-loss or take-profit triggers.
        Returns True if a sell should be forced, False otherwise.
        """
        if self.holdings > 0:
            if self.stop_loss_pct and current_price <= self.entry_price * (1 - self.stop_loss_pct):
                # Stop Loss Triggered
                self.sell(current_price, date, reason="Stop Loss")
                return True
            if self.take_profit_pct and current_price >= self.entry_price * (1 + self.take_profit_pct):
                # Take Profit Triggered
                self.sell(current_price, date, reason="Take Profit")
                return True
        return False

    def buy(self, price, date):
        """Executes a buy order."""
        if self.holdings == 0:
            # Calculate amount to invest
            invest_amount = self.cash * self.position_size_pct
            shares = invest_amount / price
            cost = shares * price

            self.cash -= cost
            self.holdings = shares
            self.entry_price = price

            self.trades.append({
                'Type': 'Buy',
                'Date': date,
                'Price': price,
                'Shares': shares,
                'Value': cost,
                'Reason': 'Signal'
            })
            # print(f"Bought {shares:.2f} shares at {price:.2f} on {date}")

    def sell(self, price, date, reason="Signal"):
        """Executes a sell order."""
        if self.holdings > 0:
            revenue = self.holdings * price
            self.cash += revenue

            self.trades.append({
                'Type': 'Sell',
                'Date': date,
                'Price': price,
                'Shares': self.holdings,
                'Value': revenue,
                'Reason': reason
            })
            # print(f"Sold {self.holdings:.2f} shares at {price:.2f} on {date} ({reason})")

            self.holdings = 0
            self.entry_price = 0

    def get_history_df(self):
        import pandas as pd
        return pd.DataFrame(self.history).set_index('Date')

    def get_trades_df(self):
        import pandas as pd
        return pd.DataFrame(self.trades)
