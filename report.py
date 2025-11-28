import numpy as np
import pandas as pd

def generate_report(portfolio):
    """
    Generates a summary report of the backtest.

    Args:
        portfolio (Portfolio): The portfolio object after backtesting.
    """
    history_df = portfolio.get_history_df()
    trades_df = portfolio.get_trades_df()

    if history_df.empty:
        print("No history to report.")
        return

    # 1. Total Return
    initial_value = portfolio.initial_capital
    final_value = history_df['Total Value'].iloc[-1]
    total_return = (final_value - initial_value) / initial_value

    # 2. Annualized Return
    # Calculate number of years
    days = (history_df.index[-1] - history_df.index[0]).days
    if days > 0:
        years = days / 365.25
        annualized_return = (final_value / initial_value) ** (1 / years) - 1
    else:
        annualized_return = 0.0

    # 3. Sharpe Ratio
    # Calculate daily returns
    daily_returns = history_df['Total Value'].pct_change().dropna()
    if daily_returns.std() > 0:
        # Assuming 252 trading days, risk-free rate = 0 for simplicity
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
    else:
        sharpe_ratio = 0.0

    # 4. Maximum Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = history_df['Total Value'].cummax()
    drawdown = (history_df['Total Value'] - peak) / peak
    max_drawdown = drawdown.min()

    # 5. Win Rate
    win_rate = 0.0
    num_trades = 0
    if not trades_df.empty:
        # Filter for Sell trades to calculate P&L per trade
        # We need to match buys and sells, but since we sell all holdings,
        # we can just look at sequential pairs or simpler:
        # Since we always close position completely, we can iterate trades.

        profits = []

        buys = trades_df[trades_df['Type'] == 'Buy']
        sells = trades_df[trades_df['Type'] == 'Sell']

        # This simple matching assumes FIFO or 1-to-1 which is true for this strategy (buy all, sell all)
        # However, we might have multiple buys if we allowed scaling in (which we don't currently)
        # Or partial sells (which we don't currently)

        # Let's iterate and match
        # Since logic is Buy -> Sell -> Buy -> Sell
        # We can zip them if counts match, or handle mismatch

        for i in range(min(len(buys), len(sells))):
            buy_val = buys.iloc[i]['Value']
            sell_val = sells.iloc[i]['Value']
            profit = sell_val - buy_val
            profits.append(profit)

        num_trades = len(profits)
        if num_trades > 0:
            winning_trades = sum(1 for p in profits if p > 0)
            win_rate = winning_trades / num_trades

    print("="*30)
    print("      Performance Report      ")
    print("="*30)
    print(f"Initial Capital:   ${initial_value:,.2f}")
    print(f"Final Value:       ${final_value:,.2f}")
    print(f"Total Return:      {total_return:.2%}")
    print(f"Annualized Return: {annualized_return:.2%}")
    print(f"Sharpe Ratio:      {sharpe_ratio:.2f}")
    print(f"Max Drawdown:      {max_drawdown:.2%}")
    print(f"Total Trades:      {num_trades}")
    print(f"Win Rate:          {win_rate:.2%}")
    print("="*30)

    return {
        'total_return': total_return,
        'annualized_return': annualized_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }
