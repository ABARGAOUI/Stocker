import datetime

from Data import get_transactions
from Data.Models.transaction_type import TType


class Transactions:
    def __init__(self, input_path):
        self.input_path = input_path
        self.content = get_transactions.get_transactions.get_revolut_transactions(input_path)
        self.tickers = list(filter(lambda x: isinstance(x, str), set(trs.ticker for trs in self.content)))
        self.start_date = min([trs.date for trs in self.content])

    def get_in_cash_amount(self):
        return sum([trans.total_amount for trans in self.content if trans.type
                    == TType.CashIn.name])

    def get_out_cash_amount(self):
        return sum([trans.total_amount for trans in self.content if trans.type
                    == TType.CashOut.name])

    def to_dict(self):
        res = {x: [] for x in set(trans.ticker for trans in self.content)}
        for trans in self.content:
            res[trans.ticker].append(trans)
        return res

