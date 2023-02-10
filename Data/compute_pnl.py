import numpy as np
from Data.Models.transaction import Transaction
from Data.Models.profit_loss import Pnl
import datetime
from Data.Models.transaction_type import TType
import yfinance as yf


def adjust_stock_splits(stock_splits, transactions):
    if isinstance(stock_splits, list) or stock_splits.empty:
        return transactions
    start_date = min([trs.date for trs in transactions])
    end_date = max([trs.date for trs in transactions])
    valid_splits = [split for split in stock_splits.items() if start_date.date() <= split[0].date() <= end_date.date()]
    for split in valid_splits:
        for transaction in transactions:
            if transaction.type in (TType.Buy.name, TType.Sell.name) and transaction.date.date() < split[0].date():
                transaction.unit_price /= float(split[1])
                transaction.quantity *= float(split[1])
    return transactions


def adjust_unit_transaction(split: tuple, transaction: Transaction):
    if transaction.date.date() < split[0].date():
        transaction.unit_price /= float(split[1])
        transaction.quantity *= float(split[1])


def get_fifo_bought_stocks(positions, exec_prices, sell_flags, position):
    sold_market_value = 0
    j = 0
    nbr_positions = 0
    last_buy_price =  0
    while nbr_positions < abs(position) and j < len(positions):
        if sell_flags[j]:
            if (nbr_positions + positions[j]) > abs(position):
                sold_market_value += (abs(position) - nbr_positions ) * exec_prices[j]
                positions[j] = positions[j] - (abs(position) - nbr_positions)
            else:
                nbr_positions += positions[j]
                sold_market_value += abs(positions[j]) * exec_prices[j]
                sell_flags[j] = False
            last_buy_price = exec_prices[j]
        j += 1
    return sold_market_value, last_buy_price


def compute_pnl(transactions, market_data):
    res = {x: [] for x in set(trans.ticker for trans in transactions.content)}
    transactions = transactions.to_dict()
    overall_r_pnl = 0
    overall_u_pnl = 0
    for key in transactions.keys():
        if key is np.NAN:
            continue
        ticker = yf.Ticker(key, session=market_data.session)
        transactions[key] = adjust_stock_splits(ticker.splits, transactions[key])
        bs_transactions = list(filter(lambda x: x.type in (TType.Buy.name, TType.Sell.name), transactions[key]))
        positions = np.array([trs.quantity if trs.type == TType.Buy.name else trs.quantity * -1 for trs in bs_transactions])
        exec_prices = np.array([trs.unit_price for trs in bs_transactions])
        sell_flags = np.array([True if pos > 0 else False for pos in positions])
        i = 0
        hold_positions = 0
        r_pnl = 0
        hold_amnt = 0
        last_buy_price = 0
        mean_buy_price = 0
        for (p, e, s) in zip(positions, exec_prices, sell_flags):
            if p > 0:
                hold_positions += p
                hold_amnt += p * e
                last_buy_price = e
                mean_buy_price = hold_amnt / hold_positions
            else:
                hold_positions += p
                if hold_positions == 0:
                    hold_amnt = 0
                else:
                    hold_amnt += p * e
                cost_amount, last_buy_price = get_fifo_bought_stocks(positions, exec_prices, sell_flags, p)
                mean_buy_price = get_updated_mean_buy_price(positions, exec_prices, sell_flags, i)
                r_pnl += -1 * (p * e) - cost_amount
            i += 1
        last_price = ticker.history(period='1d')
        close_price = -1
        u_pnl = 0
        if not last_price.empty:
            close_price = last_price['Close'].values[0]
        if close_price > 0:
            u_pnl = (close_price - mean_buy_price) * hold_positions
        overall_r_pnl += r_pnl
        overall_u_pnl += u_pnl
        pnl = Pnl(key, datetime.date.today(), r_pnl, hold_positions, hold_amnt, last_buy_price, u_pnl, close_price)
        res[key] = pnl
    return res


def get_updated_mean_buy_price(positions, exec_prices, sell_flags, index):
    j = 0
    amount = 0
    nbr_positions = 0
    while j < index:
        if sell_flags[j]:
            nbr_positions += positions[j]
            amount += positions[j] * exec_prices[j]
        j += 1
    if nbr_positions == 0:
        return 0
    return amount / nbr_positions

