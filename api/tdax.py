#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

from utility.tools import *

# DOCUMENT : https://api-docs.tdax.com
class TDAX:
    def __init__(self, key='', secret=''):
        self._key = key
        self._secret = secret

        self.ticker = []
        self.coins = {}

    '''
    Public API
    '''
    def get_ticker(self):
        pass

    def get_orderbook(self, c):
        return get('https://api.tdax.com/orders?Symbol=' + self._get_pairing_id(c))

    def get_asks_rate(self, c, invert=1000, ret=0.0):
        content = self.get_orderbook(c)
        if content:
            for rate, volume in content['asks']:
                sim_order = simulate_rate(volume, rate)

                if Decimal(sim_order) > Decimal(invert):
                    ret += float(simulate_buy(invert, rate))
                    return format_float(ret)
                else:
                    sim_buy = simulate_buy(sim_order, rate)
                    ret += float(sim_buy)
                    invert -= float(sim_order)
                #print("asks rate:{}, vol:{}, sim:({}) | inv:{}, ret:{}".format(rate, volume, sim_order, invert, ret))

    def get_bids_rate(self, c, invert=1000, ret=0.0):
        content = self.get_orderbook(c)
        if content:
            for rate, volume in content['bids']:
                sim_order = simulate_sell(volume, rate)

                if Decimal(volume) > Decimal(invert):
                    ret += float(simulate_sell(invert, rate))
                    return format_float(ret)
                else:
                    ret += float(sim_order)
                    invert = float(invert) - float(volume)
                #print("bids rate:{}, vol:{}, sim:({})| inv:{}, ret:{}".format(rate, volume, sim_order, invert, ret))

    # parser currency id
    # information : https://bx.in.th/api/pairing/
    def _pairing_list(self):
        return {
            'BTCUSDT': 'usdt_btc', 'ETHUSDT': 'usdt_eth', 'NEOUSDT':'usdt_neo'
        }

    def _get_pairing_name(self):
        return list(self._pairing_list().keys())

    def _get_pairing_id(self, currency):
        currency_id = self._pairing_list()
        if currency_id[currency]:
            return str(currency_id[currency])