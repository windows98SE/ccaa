#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

'''
* * * DEMO * * *
'''

from utility.tools import *

# DOCUMENT : https://github.com/binance-exchange/binance-official-api-docs/blob/master/rest-api.md
class BINANCE:
    def __init__(self, key='', secret=''):
        self._key = key
        self._secret = secret

        self.ticker = []
        self.coins = {}

    '''
    Public API
    '''
    def get_ticker(self):
        """Get just only top bid/ask of all currency pairs"""
        self.ticker = get('https://api.binance.com/api/v1/ticker/allBookTickers')
        if self.ticker:
            for x in self.ticker:
                pairing_id =  self._get_pairing_id(x['symbol'])
                if pairing_id:
                    self.coins[pairing_id] = {
                        'buy':x["askPrice"],
                        'sell':x["bidPrice"]
                    }

        else:
            self.ticker = []
            self.coins = {}

    # parser currency
    # todo add me plz >__<
    def _pairing_list(self):
        return {
            'BTCUSDT': 'usdt_btc', 'ETHUSDT': 'usdt_eth', 'NEOUSDT':'usdt_neo'
        }

    def _get_pairing_name(self):
        return list(self._pairing_list().keys())

    def _get_pairing_id(self, currency):
        currency_id = self._pairing_list()
        try:
            return currency_id[currency]
        except Exception:
            return None

    '''
    return self data
    '''
    def get_coin(self, c):
        if c in self.coins:
            return self.coins[c]

    '''
    DEBUG
    '''
    def dump_ticker(self):
        try:
            return self.ticker
        except Exception:
            return None

    def dump_coins(self):
        try:
            return self.coins
        except Exception:
            return None