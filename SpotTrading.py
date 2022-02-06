import hashlib
import hmac
import json
from urllib.parse import urlencode

import requests

secret = "UslHiqYHWGnZFj4ZMCHotRaIfwuj6Lxr32NawR4exBMQjT5NUpgbzlgrOI28c81H"
key = "PyKxIs4yhkXgVRpDgOHLI88eVR40TCJ8i4LoOfvBo0Fcf8YkA2y6NEdHe3jfgWra"

# https://api.binance.com/api/v3/ticker/price?symbol=BUSDUSDT
BASE_URL = "https://api.binance.com"


def current_price():
    r = requests.get(BASE_URL + '/api/v3/ticker/price?symbol=BUSDUSDT')
    values = r.json()
    values = json.dumps(values)
    values = json.loads(values)
    return float(values["price"])


def hashing(query_string):
    return hmac.new(
        secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    servertime = requests.get(BASE_URL + "/api/v3/time")
    servertimeobject = json.loads(servertime.text)
    servertimeint = servertimeobject['serverTime']
    return servertimeint


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": key}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")


def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
            BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()


def HL_price():
    # GET a https://api.binance.com//api/v3/klines?symbol=BUSDUSDT&interval=1m
    r = requests.get(BASE_URL + '/api/v3/klines?symbol=BUSDUSDT&interval=1m')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        exit(-1)
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera
        # sencilla
        values = json.dumps(values)
        values = json.loads(values)
        last_kline = values[499]
        low_price = last_kline[3]
        high_price = last_kline[2]
        return high_price, low_price


"""print(current_price())
print(HL_price()[0])
print(HL_price()[1])"""

exito = False

while not exito:
    price = current_price()
    low = float(HL_price()[1])
    print(price, " - ", str(round(low, 4)))
    if price == round(low, 4):
        params = {
            "symbol": "BUSDUSDT",
            "side": "BUY",
            "type": "LIMIT_MAKER",
            "price": low,
            "newClientOrderId": "Test1",
            "quantity": 20.00,
        }
        response = send_signed_request("POST", "/api/v3/order", params)
        print(response)
        exito = True
    print()
    print()
