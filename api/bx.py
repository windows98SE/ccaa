#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

from utility.tools import *

# DOCUMENT : https://bx.in.th/info/api/
class BX:
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
        self.ticker = get('https://bx.in.th/api/')
        if self.ticker and not 'error' in self.ticker:
            for currency in self._get_pairing_name():
                pairing_id = self._get_pairing_id(currency)
                self.coins[currency] = {
                    'buy':self.ticker[pairing_id]["orderbook"]["asks"]["highbid"],
                    'sell':self.ticker[pairing_id]["orderbook"]["bids"]["highbid"]
                }
        else:
            self.ticker = []
            self.coins = {}

    def get_orderbook(self, c):
        return get('https://bx.in.th/api/orderbook/?pairing=' + self._get_pairing_id(c))

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

    '''
    Private API
    '''
    # Get Balance
    def get_balance(self):
        return post('https://bx.in.th/api/balance/', self._build_signature())

    # Get Orders ... buy/sell
    # c=currency / t=type (buy or sell) / f=fields
    def get_order(self, c, t, f={}):
        f['type'] = t
        f['pairing'] = self._get_pairing_id(c)
        return post('https://bx.in.th/api/getorders/', self._build_signature(f))

    # Crate Order ... buy/sell
    # c=currency / a=amount / r=rate / t=type / f=fields / l=loop
    def build_order(self, c, a, r, t, f={}):
        f['pairing'] = self._get_pairing_id(c)
        f['amount'] = a
        f['rate'] = r
        f['type'] = t
        return f

    def buy(self, c, a, r, l=3):
        return self.create_order(l, self.build_order(c, a, r, t='buy'))

    def sell(self, c, a, r, l=3):
        return self.create_order(l, self.build_order(c, a, r, t='sell'))

    def create_order(self, l, f={}):
        return self.create_order_loop(l, f)

    def create_order_loop(self, l, f={}):
        resp = ''
        while l:
            time_start = time.time()
            resp = post('https://bx.in.th/api/order/', self._build_signature(f))
            if resp['order_id'] == 0:
                if resp['success'] == True:
                    break
                else:
                    l -= 1
            else:
                #return self.cancel(c, resp['order_id'])
                break

            time_end = time.time()
            delay(2 - (time_end - time_start))

        return resp

    # Canel Order
    # c=currency / o=order_id / f=fields
    def cancel(self, c, o, f={}):
        f['pairing'] = self._get_pairing_id(c)
        f['order_id'] = o
        return post('https://bx.in.th/api/cancel/', self._build_signature(f))

    # c=currency / a=amount / addr=address, bid=bank_id
    def withdrawal(self, c, a, addr='', bid='', f={}):
        f['currency'] = c.upper()
        f['amount'] = a

        if addr:
            f['address'] = addr

        if bid:
            f['bank_id'] = bid
        return post('https://bx.in.th/api/withdrawal/', self._build_signature(f))

    '''
    Utility
    '''
    # build signature
    def _build_signature(self, d={}):
        d['key'] = self._key
        d['nonce'] = nonce()
        msg = str(self._key) + str(d['nonce']) + str(self._secret)
        d['signature'] = hash(msg.encode('utf-8'), 'sha256')
        return urlencode(d)

    # parser currency id
    # information : https://bx.in.th/api/pairing/
    def _pairing_list(self):
        return {
            'thb_btc': 1,

            'btc_ltc': 2, 'btc_nmc': 3, 'btc_doge': 4, 'btc_ppc': 5, 'btc_ftc': 6,
            'btc_xpm': 7, 'btc_zec': 8, 'btc_hyp': 13, 'btc_pnd': 14, 'btc_xcn': 15,
            'btc_xpy': 17, 'btc_qrk': 19, 'btc_eth': 20,

            'thb_eth': 21, 'thb_das': 22, 'thb_rep': 23, 'thb_ngo': 24, 'thb_xrp': 25,
            'thb_omg': 26, 'thb_bch': 27, 'thb_evx': 28, 'thb_xzc': 29, 'thb_ltc': 30
        }

    def _get_pairing_name(self):
        return list(self._pairing_list().keys())

    def _get_pairing_id(self, currency):
        currency_id = self._pairing_list()
        if currency_id[currency]:
            return str(currency_id[currency])

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
