#!/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import os
import re
import sys
import threading
import time
import urllib.parse

from decimal import *

from requests import post as __post__
from requests import get as __get__

DEFAULT_TIME_OUT = 4
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

getcontext().prec = 24

'''
Time
'''
def nonce():
    return milliseconds()

def seconds():
    return int(time.time())

def milliseconds():
    return int(time.time() * 1000)

def microseconds():
    return int(time.time() * 1000000)

def delay(t):
    if t > 0:
        time.sleep(t)

def get_timestamp(format="%Y-%m-%d %H:%M:%S.%f"):
    return datetime.datetime.now().strftime(format)[:-3]

'''
encode/decode
'''
def encode(string):
    return string.encode()

def decode(string):
    return string.decode()

def json_decode(content):
    try:
        return json.loads(content, parse_float=format_float)
    except Exception:
        print("[!][json_decode] {}".format(content))
        return content

def json_encode(input):
    try:
        return json.dumps(input, separators=(',', ':'))
    except Exception:
        print("[!][json_encode] {}".format(input))
        return None

def urlencode(input):
    return urllib.parse.urlencode(input).encode("utf-8")

def hash(input, algorithm='md5', digest='hex'):
    h = hashlib.new(algorithm, input)
    if digest == 'hex':
        return h.hexdigest()
    elif digest == 'base64':
        return base64.b64encode(h.digest())
    return h.digest()

def hmac_msg(input, secret, algorithm=hashlib.sha256, digest='hex'):
    h = hmac.new(secret, input, algorithm)
    if digest == 'hex':
        return h.hexdigest()
    elif digest == 'base64':
        return base64.b64encode(h.digest())
    return h.digest()

'''
Number Notation
'''
def simulate_buy(volume, rate, fee=0.25):
    if fee:
        return format_float((Decimal(volume) / Decimal(rate)) * Decimal(simulate_fee(fee)))
    else:
        return format_float(Decimal(volume) / Decimal(rate))

def simulate_sell(volume, rate, fee=0.25):
    if fee:
        return format_float((Decimal(volume) * Decimal(rate)) * Decimal(simulate_fee(fee)))
    else:
        return format_float(Decimal(volume) * Decimal(rate))

def simulate_asks(asks, invest, ret=0.0):
    for rate, volume in asks:
        simulate_order = Decimal(volume) * Decimal(rate)
        if Decimal(invest) > Decimal(simulate_order):
            ret = Decimal(ret) + Decimal(simulate_buy(simulate_order, rate))
            invest = Decimal(invest) - Decimal(simulate_order)
        else:
            return format_float(Decimal(ret) + Decimal(simulate_buy(invest, rate)))
        #print('asks', rate, volume, simulate_order, invest, ret)

def simulate_bids(bids, invest, ret=0.0):
    for rate, volume in bids:
        if Decimal(invest) > Decimal(volume):
            ret = Decimal(ret) + Decimal(simulate_sell(volume, rate))
            invest = Decimal(invest) - Decimal(volume)
        else:
            return format_float(Decimal(ret) + Decimal(simulate_sell(invest, rate)))
        #print('bids', rate, volume, invest, ret)

def simulate_fee(fee=0.25):
    return format_float((100.00 - fee) / 100.00)

# some site : buy = ROUND_FLOOR / sell = ROUND_UP
# formal use ROUND_FLOOR
def format_float(num, ret=0, mode=ROUND_FLOOR):
    n = Decimal(str(num)).normalize()
    sign, digit, exponent = n.as_tuple()
    if exponent >= -2:
        ret = "{:0.2f}".format(n.quantize(Decimal('0.1') ** 2, rounding=mode))
    else:
        ret = "{:0.8f}".format(n.quantize(Decimal('0.1') ** 8, rounding=mode))
    return str(ret)

'''
request GET/POST
'''
def get(u):
    return _get(build_requests(u))

def post(u, d={}, h={}):
    h.update({'Content-Type': 'application/x-www-form-urlencoded'})
    return _post(build_requests(u, d, h))

def build_requests(u, d={}, h={}):
    payload = {}
    h.update(DEFAULT_HEADERS)
    if d:
        payload['data'] = d

    payload['url'] = u
    payload['headers'] = h
    payload['timeout'] = DEFAULT_TIME_OUT
    return payload

def _get(payload):
    try:
        req = __get__(**payload)
        return json_decode(req.text)
    except Exception:
        print("[!][_get] {}".format(payload))
        return None

def _post(payload):
    try:
        req = __post__(**payload)
        return json_decode(req.text)
    except Exception:
        print("[!][_post] {}".format(payload))
        return None

'''
Output
'''
def flush():
    sys.stdout.flush()

def br():
    print()

def msg(msg):
    print("{} {}".format(get_timestamp(), msg))

def msg_c(m):
    '''
    more color : https://stackoverflow.com/questions/287871/print-in-terminal-with-colors-using-python
    '''
    color = {
        '[RED]': "\x1b[1;37;41m",
        '[GREEN]': "\x1b[1;37;42m",
        '[YELLOW]': "\x1b[1;37;43m",
        '[BLUE]': "\x1b[1;37;44m",
        '[WHITE]': "\x1b[2;30;47m",
        '[END]': "\x1b[0m",
    }
    rc = re.compile('|'.join(map(re.escape, color)))
    def translate(match):
        return color[match.group(0)]
    msg(rc.sub(translate, m))

def success(m):
    msg_c("[GREEN][+][END] {}".format(m))

def warn(m):
    msg_c("[YELLOW][L][END] {}".format(m))

def err(m):
    msg_c("[RED][!][END] {}".format(m))

def log(m):
    msg_c("[BLUE][L][END] {}".format(m))

def debug(m):
    msg_c("[WHITE][D][END] {}".format(m))

def margin_color(margin):
    if float(margin) > 0:
        return "[GREEN]{:+0.2f}%[END]".format(margin)
    else:
        return "[RED]{:+0.2f}%[END]".format(margin)

def voice(msg):
    os.system('say "{}"'.format(msg))

def clear():
    os.system('cls||clear')

'''
Line
'''
def notify(msg, token):
    u = 'https://notify-api.line.me/api/notify'
    d = urlencode({'message':msg}).encode('utf-8')
    h = {
        'Authorization':'Bearer ' + token
    }
    return post(u, d, h)