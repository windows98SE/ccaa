#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

# buy bx -> sell polo
# buy btc, send btc, sell btc

from init import *

def run():
    invest = 100000
    withdrawal_fee = 0.002

    exchange1 = 'thb_btc'
    exchange2 = 'usdt_btc'

    usdt_rate = 31.50

    print("invest = {} thb".format(invest))
    buy_volume = BX().get_asks_rate(exchange1, invest)
    print("{} thb = {} btc".format(invest, buy_volume))
    total_currency = format_float(Decimal(buy_volume) - Decimal(withdrawal_fee))
    print("total = withdrawal fee (volume - {}) = {} btc".format(withdrawal_fee, total_currency))

    #-------------
    print()
    #-------------

    sell_volume = POLO().get_bids_rate(exchange2, total_currency)
    print("sell {} btc = {} usdt".format(buy_volume, sell_volume))

    #-------------
    print()
    #-------------
    to_invest = format_float(Decimal(sell_volume) * Decimal(usdt_rate))
    print("to thb = sell_volume * {} = {}".format(usdt_rate, to_invest))

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        pass