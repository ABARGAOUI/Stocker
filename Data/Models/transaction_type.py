import enum


class TTools:

    @staticmethod
    def get_transaction_type(transaction_type):
        ttype_dict = {member.name: member.value for member in TType}
        transaction_type = [key for key, value in ttype_dict.items() if transaction_type in value]
        if not transaction_type:
            return ''
        return transaction_type.pop()


class TType(enum.Enum):
    CashIn = ['CASH TOP-UP']
    CashOut = ['CASH WITHDRAWAL']
    Buy = ['BUY - LIMIT', 'BUY - MARKET']
    Sell = ['SELL - LIMIT', 'SELL - MARKET']
    Div = ['DIVIDEND']
    StockSplit = ['STOCK SPLIT']
    Fee = ['CUSTODY FEE']
    Merger = ['MERGER - STOCK']

