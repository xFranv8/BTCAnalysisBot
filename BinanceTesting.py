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

KEY = "5Fjugl2glBkbvsqHafaUwtHe3bRq1sx7cCEzN3Pmj5xOltqw2VMgLGZ0V9taxeSJ"
SECRET = "rSVN7XlLCLYpuE2DAePYOkH2zVM3flR0QHsRZwTVq0pgek8jcHX1DyxNkPUJCnba"
BASE_URL = "https://fapi.binance.com"  # production base url
# BASE_URL = 'https://testnet.binance.vision' # testnet base url

""" ======  begin of functions, you don't need to touch ====== """

def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    servertime = requests.get(BASE_URL + "/fapi/v1/time")
    servertimeobject = json.loads(servertime.text)
    servertimeint = servertimeobject['serverTime']
    return servertimeint


def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
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
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()



""" ======  end of functions ====== """

# # place an order
# if you see order response, then the parameters setting is correct
params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.001,
}

response = send_signed_request("POST", "/fapi/v1/order/test", params)
print(response)


