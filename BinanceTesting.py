import json

import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

""" This is a very simple script working on Binance API
- work with USER_DATA endpoint with no third party dependency
- work with testnet
Provide the API key and secret, and it's ready to go
Because USER_DATA endpoints require signature:
- call `send_signed_request` for USER_DATA endpoints
- call `send_public_request` for public endpoints
```python
python spot.py
```
"""


# Claves DanielMegaRabón para testear
KEY_D = "b94b3f278f28a791d7764ea0bebb38f5a73dea4e4fec7eb6cf367103eafa0bcb"
SECRET_D = "40916e9b070693fd166cbab6222c58d0290b65433ae1942aa151d44d953b258a"


BASE_URL = "https://fapi.binance.com"  # production base url
BASE_URL_TESTNET = 'https://testnet.binancefuture.com' # testnet base url

""" ======  begin of functions, you don't need to touch ====== """


def hashing(query_string):
    return hmac.new(
        SECRET_D.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    servertime = requests.get(BASE_URL + "/fapi/v1/time")
    servertimeobject = json.loads(servertime.text)
    servertimeint = servertimeobject['serverTime']
    return servertimeint


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY_D}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL_TESTNET + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


def buy(SL, TP, porcentaje=0.9):
    params = {
        "symbol": "BTCUSDT",
    }

    response = send_signed_request("GET", "/fapi/v1/ticker/price", params)
    precio = float(response['price'])

    response = send_signed_request("GET", "/fapi/v2/balance")
    balance = float(response[1]['balance']) * porcentaje

    cantidad_total = balance / precio * 5
    cantidad_total = round(cantidad_total, 3)

    params = {
        "symbol": "BTCUSDT",
        "leverage": 5,
    }

    response = send_signed_request("POST", "/fapi/v1/leverage", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "marginType": "ISOLATED",
    }

    response = send_signed_request("POST", "/fapi/v1/marginType", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "newClientOrderId": "Test1",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": str(TP),
        "newClientOrderId": "TP",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "STOP_MARKET",
        "stopPrice": str(SL),
        "newClientOrderId": "SL",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)


def sell(SL, TP, porcentaje=0.9):
    params = {
        "symbol": "BTCUSDT",
    }

    response = send_signed_request("GET", "/fapi/v1/ticker/price", params)
    precio = float(response['price'])

    response = send_signed_request("GET", "/fapi/v2/balance")
    balance = float(response[1]['balance']) * porcentaje

    cantidad_total = balance / precio * 5
    cantidad_total = round(cantidad_total, 3)

    params = {
        "symbol": "BTCUSDT",
        "leverage": 5,
    }

    response = send_signed_request("POST", "/fapi/v1/leverage", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "marginType": "ISOLATED",
    }

    response = send_signed_request("POST", "/fapi/v1/marginType", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "MARKET",
        "newClientOrderId": "Test1",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": str(TP),
        "newClientOrderId": "TP",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "STOP_MARKET",
        "stopPrice": str(SL),
        "newClientOrderId": "SL",
        "quantity": cantidad_total,
    }

    response = send_signed_request("POST", "/fapi/v1/order", params)
    print(response)


def get_PnL():
    params = {
        "symbol": "BTCUSDT",
    }

    acu = 0
    response = send_signed_request("GET", "/fapi/v1/userTrades", params)
    for position in response:
        acu = acu + float(position['realizedPnl'])

    params = {
        "symbol": "BTCUSDT",
        "incomeType": "COMMISSION",
    }
    response = send_signed_request("GET", "/fapi/v1/income", params)
    for comission in response:
        acu = acu + float(comission['income'])
    print(acu)


def existsOpenOrders():
    params = {
        "symbol": "BTCUSDT",
        "origClientOrderId": "Test1",
    }

    response = send_signed_request("GET", "/fapi/v1/order", params)

    print(response)


#buy(30000, 40000, 0.2)
#sell(40000, 30000)
#getPnL()
existsOpenOrders()

