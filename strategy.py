import pandas as pd
import numpy as np

def generate_signals(data):
    """
    Generates buy and sell signals based on a moving average crossover strategy.

    Args:
        data (pd.DataFrame): DataFrame with 'SMA_50' and 'SMA_200' columns.

    Returns:
        pd.DataFrame: The input DataFrame with an added 'Signal' column.
                      1 = Buy, -1 = Sell, 0 = No Action.
                      Also adds 'Position' column: 1 = Long, 0 = Neutral.
    """
    df = data.copy()

    # Define Position: 1 where short-term MA > long-term MA, else 0
    df['Position'] = np.where(df['SMA_50'] > df['SMA_200'], 1, 0)

    # Calculate Signal based on change in Position
    # Signal is 1 (Buy) when Position changes from 0 to 1
    # Signal is -1 (Sell) when Position changes from 1 to 0
    df['Signal'] = df['Position'].diff()

    # Shift signals by 1 day to avoid look-ahead bias.
    # We calculate signal at Close of Day T, so we can only trade at Day T+1.
    df['Signal'] = df['Signal'].shift(1)

    return df

if __name__ == "__main__":
    # Create dummy data to test
    dates = pd.date_range(start='2020-01-01', periods=10)
    data = pd.DataFrame({
        'SMA_50': [100, 102, 104, 106, 108, 105, 103, 101, 99, 97],
        'SMA_200': [103, 103, 103, 103, 103, 103, 103, 103, 103, 103]
    }, index=dates)

    # 50 > 200 happens at index 2 (104 > 103) -> Buy
    # 50 < 200 happens at index 7 (101 < 103) -> Sell

    result = generate_signals(data)
    print(result)
