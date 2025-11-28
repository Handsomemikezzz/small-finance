from portfolio import Portfolio

def backtest(data, strategy_data, initial_capital=10000, position_size_pct=1.0, stop_loss_pct=None, take_profit_pct=None):
    """
    Simulates the strategy over historical data.

    Args:
        data (pd.DataFrame): Data containing OHLC prices (must have 'Close' or 'Open').
        strategy_data (pd.DataFrame): Data containing 'Signal' column.
        initial_capital (float): Starting capital.
        position_size_pct (float): Fraction of portfolio to invest.
        stop_loss_pct (float): Stop loss percentage.
        take_profit_pct (float): Take profit percentage.

    Returns:
        Portfolio: The portfolio object containing history and trades.
    """
    portfolio = Portfolio(initial_capital, position_size_pct, stop_loss_pct, take_profit_pct)

    # Iterate through the data
    # Note: strategy_data should have same index as data

    for date, row in data.iterrows():
        price = row['Close'] # Assuming we trade at Close price for simplicity

        # 1. Update Portfolio Value
        portfolio.update_value(price, date)

        # 2. Check Risk Management (SL/TP)
        # If risk management triggers a sell, we don't process strategy buy signals on the same day (simplify)
        # But if it triggers a sell, we are flat.
        forced_sell = portfolio.check_risk_management(price, date)

        if forced_sell:
            continue

        # 3. Process Strategy Signals
        if date in strategy_data.index:
            signal = strategy_data.loc[date, 'Signal']

            if signal == 1:
                portfolio.buy(price, date)
            elif signal == -1:
                portfolio.sell(price, date)

    # Force close any open position at the end to realize P&L
    if portfolio.holdings > 0:
        last_price = data.iloc[-1]['Close']
        last_date = data.index[-1]
        portfolio.sell(last_price, last_date, reason="End of Backtest")

    return portfolio
