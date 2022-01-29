import hashlib
import hmac
import json
from urllib.parse import urlencode

import requests

apikey = "5Fjugl2glBkbvsqHafaUwtHe3bRq1sx7cCEzN3Pmj5xOltqw2VMgLGZ0V9taxeSJ"
secret = "rSVN7XlLCLYpuE2DAePYOkH2zVM3flR0QHsRZwTVq0pgek8jcHX1DyxNkPUJCnba"
testnet = "https://testnet.binancefuture.com/"
binance_api = "https://api.binance.com"

servertime = requests.get(binance_api + "/api/v3/time")
servertimeobject = json.loads(servertime.text)
servertimeint = servertimeobject['serverTime']
params = urlencode({
    "timestamp": servertimeint,
})

hashedsig = hmac.new(secret.encode('utf-8'), params.encode('utf-8'),
                     hashlib.sha256).hexdigest()

userdata = requests.post(binance_api + "/api/v3/order/test",
                        params={
                            "symbol": "BTCUSDT",
                            "side":   "BUY",
                            "type":   "MARKET",
                            "quantity": "50",
                            "timestamp": servertimeint,
                            "signature": hashedsig,
                        },
                        headers={
                            "X-MBX-APIKEY": apikey,
                        }
                        )

print(userdata)
print(userdata.text)
