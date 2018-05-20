#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

# buy bx -> sell polo
# buy btc, send btc, sell btc

from init import *

def run():
    invest = 10
    withdrawal_fee = 0.002

    exchange1 = 'btc_eth'
    exchange2 = 'btc_eth'

    print("invest = {} eth".format(invest))
    buy_volume = BX().get_bids_rate(exchange1, invest)
    print("{} eth = {} btc".format(invest, buy_volume))
    total_currency = format_float(Decimal(buy_volume) - Decimal(withdrawal_fee))
    print("total = withdrawal fee (volume - {}) = {} btc".format(withdrawal_fee, total_currency))

    #-------------
    print()
    #-------------

    sell_volume = POLO().get_asks_rate(exchange2, total_currency)
    print("sell {} btc = {} eth".format(buy_volume, sell_volume))

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        pass