import json, requests, hmac, hashlib
from urllib.parse import urlencode


class BinanceAPI:
    key = ""
    secret = ""
    BASE_URL = "https://fapi.binance.com"  # production base url
    BASE_URL_TESTNET = 'https://testnet.binancefuture.com'  # testnet base url

    def __init__(self, API_KEY, SECRET):
        self.key = API_KEY
        self.secret = SECRET

    def hashing(self, query_string):
        return hmac.new(
            self.secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def get_timestamp(self):
        servertime = requests.get(self.BASE_URL_TESTNET + "/fapi/v1/time")
        servertimeobject = json.loads(servertime.text)
        servertimeint = servertimeobject['serverTime']
        return servertimeint

    def dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update(
            {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": self.key}
        )
        return {
            "GET": session.get,
            "DELETE": session.delete,
            "PUT": session.put,
            "POST": session.post,
        }.get(http_method, "GET")

    def send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self.get_timestamp())
        else:
            query_string = "timestamp={}".format(self.get_timestamp())

        url = (
                self.BASE_URL_TESTNET + url_path + "?" + query_string + "&signature=" + self.hashing(query_string)
        )
        print("{} {}".format(http_method, url))
        params = {"url": url, "params": {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    def buy(self, SL, TP, porcentaje=0.9):
        params = {
            "symbol": "BTCUSDT",
        }

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])

        response = self.send_signed_request("GET", "/fapi/v2/balance")
        balance = float(response[1]['balance']) * porcentaje

        cantidad_total = balance / precio * 5
        cantidad_total = round(cantidad_total, 3)

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

    def sell(self, SL, TP, porcentaje=0.9):
        params = {
            "symbol": "BTCUSDT",
        }

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])

        response = self.send_signed_request("GET", "/fapi/v2/balance")
        balance = float(response[1]['balance']) * porcentaje

        cantidad_total = balance / precio * 5
        cantidad_total = round(cantidad_total, 3)

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print(response)

    def get_PnL(self):
        params = {
            "symbol": "BTCUSDT",
        }

        acu = 0
        response = self.send_signed_request("GET", "/fapi/v1/userTrades", params)
        for position in response:
            acu = acu + float(position['realizedPnl'])

        params = {
            "symbol": "BTCUSDT",
            "incomeType": "COMMISSION",
        }
        response = self.send_signed_request("GET", "/fapi/v1/income", params)
        for comission in response:
            acu = acu + float(comission['income'])
        print(acu)

    def existsOpenOrders(self):
        params = {
            "symbol": "BTCUSDT",
        }

        response = self.send_signed_request("GET", "/fapi/v2/positionRisk", params)

        if response[0]['entryPrice'] == '0.0':
            return False
        else:
            return True

    def get_klines(self, n):
        # GET a https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m
        r = requests.get(self.BASE_URL +'/fapi/v1/klines?symbol=BTCUSDT&interval=15m')
        values = r.json()

        # Compruebo si existe algun problema al realizar la peticion.
        if r.status_code != 200:
            return False, -1
        else:
            # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera
            # sencilla
            values = json.dumps(values)
            values = json.loads(values)
            return True, values[500 - n:]