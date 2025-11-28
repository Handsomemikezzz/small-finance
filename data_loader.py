import yfinance as yf
import pandas as pd

def fetch_data(ticker, start_date, end_date):
    """
    Fetches historical price data for a given ticker, cleans it, and adds moving averages.

    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: DataFrame containing OHLCV data and moving averages.
    """
    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        raise ValueError(f"No data found for {ticker}")

    # Ensure we are working with a single level index if yfinance returns MultiIndex
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)

    # Data Cleaning: Forward fill missing values
    data.ffill(inplace=True)
    data.dropna(inplace=True) # Drop any remaining NaNs at the start

    # Calculate Moving Averages
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Remove rows where MAs are NaN (first 200 rows usually)
    data.dropna(subset=['SMA_50', 'SMA_200'], inplace=True)

    return data

if __name__ == "__main__":
    try:
        df = fetch_data('AAPL', '2020-01-01', '2023-01-01')
        print("Data fetched successfully:")
        print(df.head())
        print(df.tail())
        print("\nColumns:", df.columns)
    except Exception as e:
        print(f"Error: {e}")
