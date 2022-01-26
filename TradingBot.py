import requests
import json

# Constante con el Token de la API para obtener el valor de los indicadores.
TOKEN_API_INDICATORS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM"

def getDMI():
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get('https://api.taapi.io/dmi?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return [False, -1]
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        return [True, values]

def getMA50():
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get('https://api.taapi.io/ma?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&optInTimePeriod=50')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return [False, -1]
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        return [True, values]

def getMA200():
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get('https://api.taapi.io/ma?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&optInTimePeriod=200')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return [False, -1]
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        return [True, values]

def calc_stop_loss_sells(prices):
    picos = []
    for i in range(len(prices)):
        # Si estamos en la primera vela o en la ultima, no hacemos nada, ya que no pueden ser un pico
        if (i == 0 or i == (len(prices) - 1)):
            pass
        else:
            if prices[i] > prices[i + 1] and prices[i] > prices[i - 1]:
                picos.append(prices[i])

    return picos[len(picos) - 1]


def calc_stop_loss_buys(prices):
    picos = []
    for i in range(len(prices)):
        if (i == 0 or i == (len(prices) - 1)):
            pass
        else:
            if prices[i] < prices[i + 1] and prices[i] < prices[i - 1]:
                picos.append(prices[i])

    return picos[len(picos) - 1]


# Pruebas con valores aleatorios
print(calc_stop_loss_sells([10, 15, 12, 23, 24, 20]))
print(calc_stop_loss_buys([25, 20, 15, 10, 16, 11, 9, 14, 20, 21, 16, 19]))

"""# Prueba obtener ADX.
DMI = getDMI()
if DMI[0]:
    print(DMI[1]["adx"])
    print(DMI[1]["plusdi"])
    print(DMI[1]["minusdi"])
else:
    print("Error al realizar la peticion.")"""

"""# Prueba obtener MA50.
MA50 = getMA50()
if MA50[0]:
    print(MA50[1]["value"])
else:
    print("Error al realizar la peticion.")"""

"""# Prueba obtener MA50.
MA200 = getMA200()
if MA200[0]:
    print(MA200[1]["value"])
else:
    print("Error al realizar la peticion.")"""