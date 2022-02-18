import json

import requests

class TAAPI:
    TOKEN_API = ""

    def __init__(self, TOKEN_API_INDICATORS):
        self.TOKEN_API = TOKEN_API_INDICATORS


    # Funcion para obtener el indicador DMI.
    def getDMI(self, backtracks=0):
        if backtracks == 0:
            r = requests.get('https://api.taapi.io/dmi?secret=' + self.TOKEN_API + '&exchange=binance&symbol=BTC/USDT&interval=15m')
        else:
            r = requests.get('https://api.taapi.io/dmi?secret=' + self.TOKEN_API + '&exchange=binance&symbol=BTC/USDT&interval=15m&backtracks=' + str(backtracks))
        values = r.json()

        if r.status_code != 200:
            return False, -1
        else:
            values = json.dumps(values)
            values = json.loads(values)
            return True, values
