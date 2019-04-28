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

    def get_orderbook(self, c):
        return get('https://api.binance.com/api/v1/depth?limit=50&symbol=' + str(self._get_pairing_id(c)))

    def get_asks_rate(self, c, invest=1000):
        content = self.get_orderbook(c)
        if content:
            return simulate_asks(content['asks'], invest)

    def get_bids_rate(self, c, invest=1000):
        content = self.get_orderbook(c)
        if content:
            return simulate_bids(content['bids'], invest)

    # parser currency
    # todo add me plz >__<
    # see symbol at : https://api.binance.com/api/v1/exchangeInfo
    def _pairing_list(self):
        return {
            'usdt_btc': 'BTCUSDT',
            'usdt_eth' : 'ETHUSDT',
            'usdt_neo': 'NEOUSDT',

            'eth_btc': 'ETHBTC',
            'ltc_btc': 'LTCBTC',
            'bnb_btc': 'BNBBTC',
            'neo_btc': 'NEOBTC',
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
    Utility
    '''
    # build signature
    def _build_signature(self, d={}, h={}):
        d['timestamp'] = nonce()
        p = urlencode(d)
        d['signature'] = hmac_msg(p, self._secret.encode('utf-8'), hashlib.sha256)
        h['X-MBX-APIKEY'] = self._key
        return p, h

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