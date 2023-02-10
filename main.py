# This is a sample Python script.
import datetime

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import yfinance as yf
from Data.Models.transactions import Transactions
from Data.get_market_data import CachedYahooMarketData
import Data.compute_pnl as pnl
import pandas as pd

revolut_csv_path = '/Users/medachrafbargaoui/Documents/Stocks/trading-account-statement_revolut.csv'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transactions = Transactions(input_path=revolut_csv_path)
    market_data = CachedYahooMarketData("Stocker", ' '.join(transactions.tickers), transactions.start_date.strftime("%Y-%m-%d"))
    res = pnl.compute_pnl(transactions, market_data)
    print(res)
    in_amount = transactions.get_in_cash_amount()
    out_amount = transactions.get_out_cash_amount()
    print("In flow amount in USD {}".format(in_amount))
    print("Out flow amount in USD {}".format(out_amount))
    print("Net in flow amount in USD {}".format(in_amount-out_amount))




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
