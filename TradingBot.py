from time import sleep

import requests, datetime, TelegramBot
import json

# Constante con el Token de la API para obtener el valor de los indicadores.
TOKEN_API_INDICATORS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM"
lista_DMI = []

def get_klines(n):
    # GET a https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m
    r = requests.get('https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=15m')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return [False, -1]
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        return (True, values[500-n:])


def getDMI(objetivo):
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get('https://api.taapi.io/dmi?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&backtracks=2')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return [False, -1]
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        print(values)
        lista_dmis = []
        for v in values:
            if objetivo == 0:
                lista_dmis.append(v["minusdi"])
            else:
                lista_dmis.append(v["minusdi"])

        return (True, lista_dmis)


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


def compararMedias():
    ma50 = getMA50()

    # Control de errores
    if ma50[0] == False:
        return -1

    sleep(20)

    ma200 = getMA200()
    if ma200[0] == False:
        return -1

    # Si no ha ocurrido ningun error al realizar la peticion a la API.
    if ma50[0] and ma200[0]:
        # Si la media de 50 es menor que la media de 200, devuelvo que buscamos ventas.
        if ma50[1]["value"] < ma200[1]["value"]:
            # Devuelvo un 0 que significa que buscamos ventas.
            return 0
        elif ma50[1]["value"] > ma200[1]["value"]:
            # Si no devuelvo un 1 que significa compras.
            return 1
        # Si las medias son iguales devuelvo un -1 porque no operamos.
        return -1


def calc_take_profit(SL, open_price):
    # open_price = get_klines(1)[1][1]
    porcentaje_TP = (((SL * 100) / open_price) - 100) / 2
    print(porcentaje_TP)
    take_profit = ((100 - porcentaje_TP) / 100) * open_price
    return take_profit



"""
# Pruebas con valores aleatorios
print(calc_stop_loss_sells([10, 15, 12, 23, 24, 20]))
print(calc_stop_loss_buys([25, 20, 15, 10, 16, 11, 9, 14, 20, 21, 16, 19]))
"""

"""# Prueba obtener ADX.
DMI = getDMI()
if DMI[0]:
    print(DMI[1]["adx"])
    print(DMI[1]["plusdi"])
    print(DMI[1]["minusdi"])
else:
    print("Error al realizar la peticion.")
# Prueba obtener MA50.
MA50 = getMA50()
if MA50[0]:
    print(MA50[1]["value"])
else:
    print("Error al realizar la peticion.")
# Prueba obtener MA200.
MA200 = getMA200()
if MA200[0]:
    print(MA200[1]["value"])
else:
    print("Error al realizar la peticion.")
klines = get_klines(8)
list_lows = []
for kline in klines[1]:
    list_lows.append(kline[2])
print(calc_stop_loss_sells(list_lows))"""

operamos = False
medias_comprobadas = False
saved_adx = False

while True:
    minutos = datetime.datetime.now().minute

    # Comprobamos la posicion de las dos medias a las horas correspondientes.
    if (minutos == 12) or (minutos == 27) or (minutos == 42) or (minutos == 57):
        # -1 Medias Iguales, no hacemos nada
        # 0 Buscamos ventas
        # 1 Buscamos compras.
        if not medias_comprobadas:
            objetivo = compararMedias()
            medias_comprobadas = True



    if (minutos == 14) or (minutos == 28) or (minutos == 44) or (minutos == 58):
        if not saved_adx:
            lista_DMI = getDMI(objetivo)[1]
            saved_adx = True
        if lista_DMI[0] > 25 and lista_DMI[1] < 25 and objetivo != -1:
                operamos = True
        else:
            print("No hay oportunidad")
            print(lista_DMI)



    if (minutos == 15) or (minutos == 30) or (minutos == 45) or (minutos == 00):
        if operamos:
            last_klines = get_klines(15)
            open_price = last_klines[1][14][1]
            lows = []
            for kline in last_klines[1]:
                lows.append(kline[3])
            if objetivo == 1:
                # Estamos en compras
                stop_loss = calc_stop_loss_buys(lows, open_price)
                take_profit = calc_take_profit(stop_loss)
            else:
                # Estamos en ventas
                stop_loss = calc_stop_loss_sells(lows, open_price)
                take_profit = calc_take_profit(stop_loss)

            message = "Empezamos operación con fecha: " + str(datetime.datetime.now()) + '\n' + \
                      "Precio de apertura de la operación: " + str(open_price) + '\n' +\
                      "STOP LOSS: " + str(stop_loss) + '\n' +\
                      "TAKE PROFIT: " + str(take_profit)

            print(message)
            TelegramBot.send_message(message)
        saved_adx = False
        medias_comprobadas = False


"""if objetivo == -1:
        print("Error al realizar las peticiones.")
    elif objetivo == 0:
        print("Buscamos ventas")
    elif objetivo == 1:
        print("Buscamos compras")

    sleep(20)"""
