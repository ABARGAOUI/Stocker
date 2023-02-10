from Data.Models.transaction import Transaction
import pandas as pd
import logging


class get_transactions:
    @staticmethod
    def get_revolut_transactions(path):
        transactions = []
        transactions_df = pd.read_csv(path)
        for ind in transactions_df.index:
            trs = Transaction(date=transactions_df['Date'][ind], ticker=transactions_df['Ticker'][ind],
                              type=transactions_df['Type'][ind],
                              quantity=transactions_df['Quantity'][ind],
                              unit_price=transactions_df['Price per share'][ind],
                              total_amount=transactions_df['Total Amount'][ind],
                              currency=transactions_df['Currency'][ind]
                              )
            if trs.type == '':
                logging.warning("The transaction type of transaction line {} of type \'{}\' Please check your input!".format(ind, transactions_df['Type'][ind]))
            transactions.append(trs)
        return transactions

