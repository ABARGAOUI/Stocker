from Data.Models.transaction_type import TTools, TType
from datetime import datetime


class Transaction:
    def __init__(self, date, ticker, type, quantity, unit_price, total_amount, currency):
        self.date = datetime.strptime(date.split('T')[0], '%Y-%m-%d')
        self.ticker = ticker
        self.type = TTools.get_transaction_type(type)
        self.quantity = float(quantity)
        self.unit_price = float(str(unit_price).split('$').pop().replace(',', '')) if unit_price != '' else 0
        self.total_amount = float(str(total_amount).split('$').pop().replace(',', '')) if unit_price != '' else 0
        self.currency = currency

    def get_type(self):
        return self.type

    def __str__(self):
        if self.type in [TType.Buy.name, TType.Sell.name]:
            return '{} transaction on {} at price {} quantity {}'.format(self.type, self.ticker, self.unit_price, self.quantity)
        elif self.type in [TType.CashIn.name, TType.CashOut.name]:
            return '{} transaction of an amount {}'.format(self.type, self.total_amount)



