#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

# buy polo -> sell bx
# buy btc, send btc, sell btc

from init import *

def run():
    invest = 5000
    withdrawal_fee = 0.002

    exchange1 = 'usdt_btc'
    exchange2 = 'thb_btc'

    usdt_rate = 31.50

    print("invest = {}".format(invest))
    buy_volume = POLO().get_asks_rate(exchange1, invest)
    print("buy_volume = {}".format(buy_volume))
    total_currency = format_float(Decimal(buy_volume) - Decimal(withdrawal_fee))
    print("total volume = withdrawal fee (volume - {}) = {}".format(withdrawal_fee, total_currency))

    #-------------
    print()
    #-------------

    sell_volume = BX().get_bids_rate(exchange2, total_currency)
    print("sell_volume = {}".format(sell_volume))

    #-------------
    print()
    #-------------
    to_invest = format_float(Decimal(sell_volume) / Decimal(usdt_rate))
    print("to thb = sell_volume / {} = {}".format(usdt_rate, to_invest))

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        pass