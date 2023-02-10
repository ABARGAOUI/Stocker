
class Pnl:

    def __init__(self, ticker, date, realized_pnl, open_positions_quantity, hold_amount, last_buy_price, unrealized_pnl, last_close):
        self.realized_pnl = realized_pnl
        self.open_positions_quantity = open_positions_quantity
        self.unrealized_pnl = unrealized_pnl
        self.ticker = ticker
        self.date = date
        self.hold_amount = hold_amount
        self.last_buy_price = last_buy_price
        self.last_close = last_close
        self.total_value = last_close * open_positions_quantity

    def __str__(self):
        return "realized_pnl = {}/ open_positions_quantity = {}/ hold_amount = {}".\
            format(self.realized_pnl, self.open_positions_quantity, self.hold_amount)
