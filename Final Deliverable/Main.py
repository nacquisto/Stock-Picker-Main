from Classes.StockSelection import StockSelection
from Classes.DateSelection import DateSelection
from Classes.FetchData import FetchData
from Classes.GPTStock import GPT_Stock
from Classes.Analysis import Portfolio, Optimizer


def main():
    # Initialize the StockSelection and DateSelection classes
    stock_selector = StockSelection()
    date_selector = DateSelection()

    # User selects two stocks
    selected_stocks = stock_selector.select_stocks()
    stock_symbols = [stock['Symbol'] for stock in selected_stocks]

    # User selects start and end dates
    start_date, end_date = date_selector.select_dates()

    assets = stock_symbols
    percentages = [0.5, 0.5]

    # Initialize the FetchData class with the selected stocks and dates
    data_fetcher = FetchData(stock_symbols, start_date, end_date)

    # Fetch and process the stock data
    data_fetcher.fetch_stock_data()

    # Get and print the processed stock data
    stock_data = data_fetcher.get_stock_data()
    for symbol, data in stock_data.items():
        print(f"\nData for {symbol}:")
        print(data)

    # Initialize the GPT_Stock class and get the comparison analysis
    gpt_stock = GPT_Stock(stock_symbols)
    comparison_analysis = gpt_stock.get_comparison_analysis()
    print("\nComparison Analysis:")
    print(comparison_analysis)

    my_portfolio = Portfolio(assets, percentages, start_date)
    my_optimizer = Optimizer(my_portfolio)

    # Display the overlapping stock charts
    my_portfolio.plot_stock_chart()

    # Display the theoretical returns
    my_portfolio.get_theoretical_returns()

    # Run the optimization simulations
    my_optimizer.run_optimization_simulations()

    # Get and display the maximum Sharpe Ratio information
    max_sr_ret, max_sr_vol = my_optimizer.get_max_sharpe_ratio_info()
    print(f"Max Sharpe Ratio return: {max_sr_ret}, volatility: {max_sr_vol}")

    # Display the efficient frontier graph
    my_optimizer.graph_efficient_frontier()

    # Generate and display risk parity
    my_optimizer.generate_risk_parity()
    my_optimizer.graph_asset_risk()
    my_optimizer.graph_risk_parity_allocation()

    # Print the conclusion
    my_optimizer.get_conclusion()

if __name__ == "__main__":
    main()