import pandas as pd
import yfinance as yf
import numpy as np

class FetchData:
    def __init__(self, symbols, start_date, end_date):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = {}

    # Fetch the stock data from Yahoo Finance
    def fetch_stock_data(self):
        for symbol in self.symbols:
            data = yf.download(symbol, start=self.start_date, end=self.end_date)
            self.stock_data[symbol] = data
        self.calculate_indicators()

    # Return the fetched stock data
    def get_stock_data(self):
        return self.stock_data

    # Calculate indicators for the fetched stock data
    def calculate_indicators(self):
        stock_prices = []

        # Reset the index for each stock data and append it to the stock prices list
        for symbol, data in self.stock_data.items():
            data = data.reset_index()
            data['Symbol'] = symbol
            stock_prices.append(data[['Symbol', 'Date', 'Adj Close', 'Volume']])

        # Concatenate all the stock data into a single DataFrame and rename the columns
        stock_prices_df = pd.concat(stock_prices)
        stock_prices_df = stock_prices_df.rename(columns={"Adj Close": "Price"})
        stock_list = stock_prices_df['Symbol'].unique().tolist()

        # Define constants for the moving average window and the number of trading days in a year
        MAwindow = 10
        StockDaysInYear = 250

        # Create an empty DataFrame to store the end of day data for the stocks
        stocks_eod_data = pd.DataFrame(columns=['Symbol', 'Date', 'Price', 'Volume', 'Log Return', 'Std Dev', 'Volatility', 'ADV', 'MDV'])
        
        # Calculate the indicators for each stock and append the data to the stocks_eod_data DataFrame
        for stock in stock_list:
            temp_df = stock_prices_df[stock_prices_df['Symbol'] == stock].copy()
            temp_df["Log Return"] = np.log(temp_df["Price"] / temp_df["Price"].shift(-1))
            temp_df["Std Dev"] = temp_df["Log Return"].rolling(MAwindow).std().shift(-MAwindow + 1)
            temp_df["Volatility"] = temp_df["Std Dev"] * StockDaysInYear**0.5
            temp_df["ADV"] = temp_df["Volume"].rolling(MAwindow).mean().shift(-MAwindow + 1).round(2)
            temp_df["MDV"] = temp_df["Volume"].rolling(MAwindow).median().shift(-MAwindow + 1).round(2)
            stocks_eod_data = pd.concat([temp_df, stocks_eod_data], join="inner")

        # Sort the stocks_eod_data DataFrame by symbol and date and fill any missing values with a placeholder
        stocks_eod_data = stocks_eod_data.sort_values(by=["Symbol", "Date"], ascending=[True, False])
        stocks_eod_data.fillna("#N/A", inplace=True)

        # Update the stock_data attribute with the calculated indicators
        self.stock_data = {symbol: stocks_eod_data[stocks_eod_data['Symbol'] == symbol] for symbol in stock_list}