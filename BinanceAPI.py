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
        servertime = requests.get(self.BASE_URL + "/fapi/v1/time")
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
                self.BASE_URL + url_path + "?" + query_string + "&signature=" + self.hashing(query_string)
        )
        print("{} {}".format(http_method, url))
        params = {"url": url, "params": {}}
        response = self.dispatch_request(http_method)(**params)
        return response.json()

    def buy(self, SL, TP, porcentaje=0.9):
        params = {
            "symbol": "BTCUSDT",
        }
        print("")
        print("[INICIO FUNCION BUY DE BINANCEAPI]\n")

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])
        print("Precio de compra: " + str(precio) + "\n")

        response = self.send_signed_request("GET", "/fapi/v2/balance")
        usdt = 0
        for r in response:
            if r['asset'] == 'USDT':
                usdt = float(r['balance'])
        print("Balance de la cuenta: " + str(usdt) + "\n")

        cantidad_total = (usdt / precio) * 5
        cantidad_total = round(cantidad_total*porcentaje, 3)

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print("[Ajuste de apalancamiento]\n")
        print(response)
        print("[Fin de ajuste de apalancamiento]")

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print("[Ajuste de tipo de margin (Aislado o cruzado)]")
        print(response)
        print("[Fin de ajuste de tipo de margin]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de compra]")
        print(response)
        print("[Fin de peticion de compra]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Take Profit]")
        print(response)
        print("[Fin de peticion de take profit]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Stop Loss]")
        print(response)
        print("[Fin de peticion de Stop Loss]")
        print("[FIN FUNCION BUY DE BINANCEAPI]\n")
        print("")

        return cantidad_total

    def buyV2(self, SL, TP, cantidad_total):
        params = {
            "symbol": "BTCUSDT",
        }

        print("")
        print("[INICIO FUNCION BUYV2 DE BINANCEAPI]\n")

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])
        print("Precio de compra: " + str(precio) + "\n")

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print("[Ajuste de apalancamiento]\n")
        print(response)
        print("[Fin de ajuste de apalancamiento]")

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print("[Ajuste de tipo de margin (Aislado o cruzado)]")
        print(response)
        print("[Fin de ajuste de tipo de margin]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de compra]")
        print(response)
        print("[Fin de peticion de compra]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Take Profit]")
        print(response)
        print("[Fin de peticion de take profit]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Stop Loss]")
        print(response)
        print("[Fin de peticion de Stop Loss]")
        print("[FIN FUNCION BUYV2 DE BINANCEAPI]\n")
        print("")

    def sell(self, SL, TP, porcentaje=0.9):
        params = {
            "symbol": "BTCUSDT",
        }

        print("")
        print("[INICIO FUNCION SELL DE BINANCEAPI]\n")

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])
        print("Precio de venta: " + str(precio) + "\n")

        response = self.send_signed_request("GET", "/fapi/v2/balance")
        usdt = 0
        for r in response:
            if r['asset'] == 'USDT':
                usdt = float(r['balance'])
        print("Balance de la cuenta: " + str(usdt) + "\n")

        cantidad_total = (usdt / precio) * 5
        cantidad_total = round(cantidad_total * porcentaje, 3)

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print("[Ajuste de apalancamiento]\n")
        print(response)
        print("[Fin de ajuste de apalancamiento]")

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print("[Ajuste de tipo de margin (Aislado o cruzado)]")
        print(response)
        print("[Fin de ajuste de tipo de margin]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de venta]")
        print(response)
        print("[Fin de peticion de venta]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Take Profit]")
        print(response)
        print("[Fin de peticion de take profit]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Stop Loss]")
        print(response)
        print("[Fin de peticion de Stop Loss]")
        print("[FIN FUNCION SELL DE BINANCEAPI]\n")
        print("")

        return cantidad_total

    def sellV2(self, SL, TP, cantidad_total):
        params = {
            "symbol": "BTCUSDT",
        }

        print("")
        print("[INICIO FUNCION SELLV2 DE BINANCEAPI]\n")

        response = self.send_signed_request("GET", "/fapi/v1/ticker/price", params)
        precio = float(response['price'])
        print("Precio de venta: " + str(precio) + "\n")

        params = {
            "symbol": "BTCUSDT",
            "leverage": 5,
        }

        response = self.send_signed_request("POST", "/fapi/v1/leverage", params)
        print("[Ajuste de apalancamiento]\n")
        print(response)
        print("[Fin de ajuste de apalancamiento]")

        params = {
            "symbol": "BTCUSDT",
            "marginType": "ISOLATED",
        }

        response = self.send_signed_request("POST", "/fapi/v1/marginType", params)
        print("[Ajuste de tipo de margin (Aislado o cruzado)]")
        print(response)
        print("[Fin de ajuste de tipo de margin]")

        params = {
            "symbol": "BTCUSDT",
            "side": "SELL",
            "type": "MARKET",
            "newClientOrderId": "Test1",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de venta]")
        print(response)
        print("[Fin de peticion de venta]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": str(TP),
            "newClientOrderId": "TP",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Take Profit]")
        print(response)
        print("[Fin de peticion de take profit]")

        params = {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "STOP_MARKET",
            "stopPrice": str(SL),
            "newClientOrderId": "SL",
            "quantity": cantidad_total,
        }

        response = self.send_signed_request("POST", "/fapi/v1/order", params)
        print("[Peticion de Stop Loss]")
        print(response)
        print("[Fin de peticion de Stop Loss]")
        print("[FIN FUNCION SELLV2 DE BINANCEAPI]\n")
        print("")

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
        r = requests.get(self.BASE_URL + '/fapi/v1/klines?symbol=BTCUSDT&interval=15m')
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

    def cancelAllOrders_TESTNET(self, cantidad_a_vender, objetivo):

        params = {
            "symbol": "BTCUSDT",
        }
        response = self.send_signed_request("DELETE", "/fapi/v1/allOpenOrders", params)
        print("")
        print("[BORRAMOS LAS ORDENES QUE HAYAN ABIERTAS. ORDENES != POSICIONES]")
        print(response)
        print("")

        if objetivo == 1:
            self.sellV2(150000, 2000, cantidad_a_vender)
        else:
            self.buyV2(2000, 150000, cantidad_a_vender)

        response = self.send_signed_request("DELETE", "/fapi/v1/allOpenOrders", params)
        print("[BORRAMOS LAS ORDENES QUE HAYAN ABIERTAS. ORDENES != POSICIONES]")
        print(response)
        print("")

    def cancelAllOrders(self, cantidad_a_vender, objetivo):

        params = {
            "symbol": "BTCUSDT",
        }
        response = self.send_signed_request("DELETE", "/fapi/v1/allOpenOrders", params)
        print("")
        print("[BORRAMOS LAS ORDENES QUE HAYAN ABIERTAS. ORDENES != POSICIONES]")
        print(response)
        print("")
