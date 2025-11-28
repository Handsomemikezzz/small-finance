import argparse
from data_loader import fetch_data
from strategy import generate_signals
from backtester import backtest
from report import generate_report

def main():
    parser = argparse.ArgumentParser(description='Small-Finance Quantitative Trading System')
    parser.add_argument('--ticker', type=str, default='AAPL', help='Stock ticker symbol')
    parser.add_argument('--start', type=str, default='2015-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2023-01-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--capital', type=float, default=10000.0, help='Initial capital')
    parser.add_argument('--sl', type=float, default=None, help='Stop loss percentage (e.g. 0.05 for 5%)')
    parser.add_argument('--tp', type=float, default=None, help='Take profit percentage (e.g. 0.10 for 10%)')

    args = parser.parse_args()

    try:
        # Step 1 & 2: Data Collection and Cleaning
        print(f"\nStep 1: Fetching data for {args.ticker}...")
        data = fetch_data(args.ticker, args.start, args.end)
        print(f"Loaded {len(data)} rows of data.")

        # Step 3: Strategy
        print("\nStep 2: Generating Strategy Signals...")
        strategy_data = generate_signals(data)

        # Step 4 & 5: Backtesting and Portfolio Management
        print("\nStep 3: Running Backtest...")
        portfolio = backtest(
            data,
            strategy_data,
            initial_capital=args.capital,
            stop_loss_pct=args.sl,
            take_profit_pct=args.tp
        )

        # Step 6: Reporting
        print("\nStep 4: Generating Report...")
        generate_report(portfolio)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
