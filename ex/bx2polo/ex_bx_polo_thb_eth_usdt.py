#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

# buy bx -> sell polo
# buy eth, send eth, sell eth

from init import *

def run():
    invest = 100000
    withdrawal_fee = 0.0005

    exchange1 = 'thb_eth'
    exchange2 = 'usdt_eth'

    usdt_rate = 31.50

    print("invest = {} thb".format(invest))
    buy_volume = BX().get_asks_rate(exchange1, invest)
    print("{} thb = {} eth".format(invest, buy_volume))
    total_currency = format_float(Decimal(buy_volume) - Decimal(withdrawal_fee))
    print("total = withdrawal fee (volume - {}) = {} eth".format(withdrawal_fee, total_currency))

    #-------------
    print()
    #-------------

    sell_volume = POLO().get_bids_rate(exchange2, total_currency)
    print("sell {} eth = {} usdt".format(buy_volume, sell_volume))

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