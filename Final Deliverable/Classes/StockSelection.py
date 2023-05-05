import pandas as pd

class StockSelection:
    def __init__(self, csv_path="CSV/SP500.csv"):
        self.csv_path = csv_path
        self.stock_data = None
        self.load_stock_data()

    # Load stock data from a CSV file containing S&P 500 companies
    def load_stock_data(self):
        self.stock_data = pd.read_csv(self.csv_path)

    # Display the stocks with their symbols and names
    def display_stocks(self):
        print(self.stock_data[["Symbol", "Name"]])

    # Get stock information for a given stock symbol
    def get_stock(self, stock_symbol):
        stock = self.stock_data[self.stock_data["Symbol"] == stock_symbol]
        if not stock.empty:
            return stock[["Symbol", "Name"]].iloc[0]
        else:
            return None

    # Allow the user to select two stocks from the list
    def select_stocks(self):
        print("Please select two stocks from the list:")
        self.display_stocks()

        stocks = []
        while len(stocks) < 2:
            stock_symbol = input("Enter stock symbol: ").strip().upper()
            stock = self.get_stock(stock_symbol)
            if stock is not None:
                stocks.append(stock)
                print(f"Selected: {stock['Symbol']} - {stock['Name']}")
            else:
                print("Invalid stock symbol. Please try again.")

        return stocks