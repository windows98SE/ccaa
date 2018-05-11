#!/usr/bin/env python3
# -*- encoding : utf-8 -*-

from utility.tools import *

# DOCUMENT : https://poloniex.com/support/api/
class POLO:
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
        self.ticker = get('https://poloniex.com/public?command=returnTicker')
        if self.ticker:
            for currency in self._get_pairing_name():
                pairing_name = currency.upper()
                self.coins[currency] = {
                    'buy':self.ticker[pairing_name]["lowestAsk"],
                    'sell':self.ticker[pairing_name]["highestBid"]
                }
        else:
            self.ticker = []
            self.coins = {}

    def get_orderbook(self, c):
        return get('https://poloniex.com/public?command=returnOrderBook&currencyPair='+ str(c.upper()) +'&depth=30')

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
    def get_balance(self, f={}):
        f['command'] = 'returnBalances'
        p, h = self._build_signature(f)
        return post('https://poloniex.com/tradingApi', p, h)

    # Get Orders ... buy/sell
    # c=currency / f=fields
    def get_order(self, c='all', f={}):
        f['currencyPair'] = c.upper()
        f['command'] = 'returnOpenOrders'
        p, h = self._build_signature(f)
        return post('https://poloniex.com/tradingApi', p, h)

    # Crate Order ... buy/sell
    # c=currency / a=amount / r=rate / t=type / f=fields / l=loop
    def build_order(self, c, a, r, t, f={}):
        f['currencyPair'] = c.upper()
        f['amount'] = a
        f['rate'] = r
        f['command'] = t
        return f

    def buy(self, c, a, r):
        return self.create_order(self.build_order(c, a, r, t='buy'))

    def sell(self, c, a, r):
        return self.create_order(self.build_order(c, a, r, t='sell'))

    def create_order(self, f={}):
        p, h = self.build_signature(f)
        return post('https://poloniex.com/tradingApi', p, h)

    # Canel Order
    # o=orderNumber / f=fields
    def cancel(self, o, f={}):
        f['command'] = 'cancelOrder'
        f['orderNumber'] = o
        p, h = self.build_signature(f)
        return post(build_requests('https://poloniex.com/tradingApi', p, h))

    # c=currency / a=amount / addr=address, pId(For XMR withdrawals)
    def withdraw(self, c, a, addr, pId='', f={}):
        f['command'] = 'withdraw'
        f['currency'] = c.upper()
        f['amount'] = a
        f['address'] = addr
        if pId:
            f['paymentId'] = pId
        p, h = self.build_signature(f)
        return post('https://poloniex.com/tradingApi', p, h)

    '''
    Utility
    '''
    # build signature
    def _build_signature(self, d={}, h={}):
        d['nonce'] = nonce()
        p = urlencode(d)
        h['Key'] = self._key
        h['Sign'] = hmac_msg(p, self._secret.encode('utf-8'), hashlib.sha512)
        return p, h

    # parser currency
    def _pairing_list(self):
        return {
            'usdt_btc':121, 'usdt_dash':122, 'usdt_ltc':123,
            'usdt_nxt':124, 'usdt_str':125, 'usdt_xmr':126,
            'usdt_xrp':127, 'usdt_eth':149, 'usdt_etc':173,
            'usdt_rep':175, 'usdt_zec':180, 'usdt_bch':191,

            'btc_bcn':7, 'btc_bela':8, 'btc_blk':10,
            'btc_btcd':12, 'btc_btm': 13, 'btc_bts':14,
            'btc_burst':15, 'btc_clam':20, 'btc_dash':24,
            'btc_dgb':25, 'btc_doge':27, 'btc_emc2':28,
            'btc_fldc':31, 'btc_flo':32, 'btc_game':38,
            'btc_grc':40, 'btc_huc':43, 'btc_ltc':50,
            'btc_maid':51, 'btc_omni':58, 'btc_nav':61,
            'btc_neos':63, 'btc_nmc':64, 'btc_nxt':69,
            'btc_pink':73, 'btc_pot':74, 'btc_ppc':75,
            'btc_ric': 83, 'btc_str':89, 'btc_sys':92,
            'btc_via':97, 'btc_xvc':98, 'btc_vrc':99,
            'btc_xbc':104, 'btc_xcp':108, 'btc_xem':112,
            'btc_xmr':114, 'btc_xpm':116, 'btc_xrp':117,
            'btc_eth':148,

            'eth_lsk':166, 'eth_steem':169, 'eth_etc':172,
            'eth_rep':176, 'eth_zec':179, 'eth_gnt':186,
            'eth_gno':188, 'eth_bch':190, 'eth_zrx':193,
            'eth_cvc':195, 'eth_omg':197, 'eth_gas':199,

            'xmr_bcn':129, 'xmr_blk':130, 'xmr_btcd':131,
            'xmr_dash':132, 'xmr_ltc':137, 'xmr_maid':138,
            'xmr_nxt':140, 'xmr_zec':181
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
