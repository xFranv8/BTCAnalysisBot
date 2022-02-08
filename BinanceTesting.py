import datetime, BinanceAPI, numpy as np
import json
from time import sleep

import requests
from pytz import timezone
from pyfiglet import Figlet


def banner():
    custom_fig = Figlet(font='big')
    print(custom_fig.renderText('BTC Trading Bot'))
    print("Bot inicializado ....")


"""banner()
operamos = False
medias_comprobadas = False
saved_adx = False
pruebas = False
acumulado = [0]
objetivo = -1

BinanceAPI = BinanceAPI.BinanceAPI("b94b3f278f28a791d7764ea0bebb38f5a73dea4e4fec7eb6cf367103eafa0bcb",
                                   "40916e9b070693fd166cbab6222c58d0290b65433ae1942aa151d44d953b258a")"""


def calc_take_profit(SL, open_price):
    # open_price = get_klines(1)[1][1]
    porcentaje_TP = (((SL * 100) / open_price) - 100) / 2
    take_profit = ((100 - porcentaje_TP) / 100) * open_price
    return take_profit


def compararMedias():
    return 1


"""def result(stop_loss, take_profit, open_price, objetivo, acumulado):
    # Calculo los % para mostrarlos luego segun el open price, el stop_loss y el take_profit
    porcentaje_SL = 100 - ((stop_loss * 100) / open_price)
    porcentaje_TP = ((take_profit * 100) / open_price) - 100

    # Seteo una variable booleana a False para que hasta que no se haya terminado la operacion siga monitorizando si toca TP o SL.
    exito = False

    while not exito:
        # Obtengo la ultima vela que se ha formado constantemente hasta que el High o el Low superen al SL o al TP.
        last_line = (38977.2, 38319.25)

        # Si estamos en compras el High debe ser superior al TP para ganar o el Low debe ser inferior al SL para perder.
        if objetivo == 1:
            # En este caso el High es superior o igual al TP, por lo que habriamos ganado.
            if (last_line[0] >= take_profit):
                message = "Operacion ganada!!!\n" + "% Realizado: " + str(porcentaje_TP)
                acumulado[0] = acumulado[0] + float(porcentaje_TP)
                TelegramBot.send_message(message)
                exito = True
            # En este caso el Low es inferior o igual al SL por lo que hubieramos perdido.
            elif (last_line[1] <= stop_loss):
                message = "Operacion perdida!!!\n" + "% Realizado: " + str(porcentaje_SL)
                acumulado[0] = acumulado[0] - float(porcentaje_SL)
                TelegramBot.send_message(message)
                exito = True
        # Si estamos aqui es porque objetivo es igual a 0 lo que significa que estamos en ventas y es al reves.
        else:
            # En este caso el Low es inferior o igual al TP profit por lo que hubieramos ganado.
            if (last_line[1] <= take_profit):
                message = "Operacion ganada!!!\n" + "% Realizado: " + str(porcentaje_TP)
                acumulado[0] = acumulado[0] + float(porcentaje_TP)
                TelegramBot.send_message(message)
                exito = True
            # En este caso el High es superior o igual al SL por lo que hubieramos perdido
            elif (last_line[0] >= stop_loss):
                message = "Operacion perdida!!!\n" + "% Realizado: " + str(porcentaje_SL)
                acumulado[0] = acumulado[0] - float(porcentaje_SL)
                TelegramBot.send_message(message)
                exito = True
    message = "% Acumulado: " + str(acumulado[0])
    TelegramBot.send_message(message)"""


def cancelAllOrders():
    params = {
        "symbol": "BTCUSDT",
    }

    response = BinanceAPI.send_signed_request("DELETE", "/fapi/v1/allOpenOrders", params)
    print(response)


"""while True:
    madrid = timezone('Europe/Madrid')
    minutos = datetime.datetime.now(madrid).minute
    # Comprobamos la posicion de las dos medias a las horas correspondientes.
    # -1 Medias Iguales, no hacemos nada
    # 0 Buscamos ventas
    # 1 Buscamos compras.
    if not medias_comprobadas:
        objetivo = compararMedias()
        medias_comprobadas = True

    if not saved_adx:
        lista_DMI = [40.00, 21.65]
        saved_adx = True
    if lista_DMI[0] > 25.00 > lista_DMI[1] and objetivo != -1:
        operamos = True

    if operamos and not BinanceAPI.existsOpenOrders():
        # last_klines = BinanceAPI.get_klines(15)
        open_price = 38927.15
        aux = []
        if objetivo == 1:
            # Estamos en compras
            stop_loss = float(38465.24)
        else:
            # Estamos en ventas
            # stop_loss = float(calc_stop_loss_sells(aux))
            pass
        take_profit = calc_take_profit(stop_loss, open_price)

        message = "Empezamos operación con fecha: " + str(datetime.datetime.now(madrid)) + '\n' + \
                  "Precio de apertura de la operación: " + str(open_price) + '\n' + \
                  "STOP LOSS: " + str(stop_loss) + '\n' + \
                  "TAKE PROFIT: " + str(round(take_profit))
        if objetivo == 1:
            # Estamos en compras
            BinanceAPI.buy(stop_loss, take_profit)
        else:
            # Estamos en ventas
            # stop_loss = float(calc_stop_loss_sells(aux))
            pass
        print(message)
        print(TelegramBot.send_message(message))
        operamos = False
        input()
        result(stop_loss, take_profit, open_price, objetivo, [0])
        input()

        # Inicializo el hilo que se va a encargar de comprobar que ha pasado con la operacion.
        resultado_operacion = threading.Thread(target=result, args=(stop_loss, take_profit, open_price, objetivo, acumulado))
        resultado_operacion.start()

        # Esperamos hasta que el hilo haya terminado, cuando haya terminado continua la ejecucion.
            threading.Thread.join()
        saved_adx = False
        medias_comprobadas = False
    else:
        print("orden ya abierta")
        input()"""

"""def sell(SL, TP, porcentaje=0.9):
    params = {
        "symbol": "BTCUSDT",
    }

    response = BinanceAPI.send_signed_request("GET", "/fapi/v1/ticker/price", params)
    precio = float(response['price'])

    response = BinanceAPI.send_signed_request("GET", "/fapi/v2/balance")
    balance = float(response[1]['balance']) * porcentaje

    cantidad_total = balance / precio * 5
    cantidad_total = round(cantidad_total, 3)

    params = {
        "symbol": "BTCUSDT",
        "leverage": 5,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/leverage", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "marginType": "ISOLATED",
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/marginType", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "MARKET",
        "newClientOrderId": "Test1",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": str(TP),
        "newClientOrderId": "TP",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "STOP_MARKET",
        "stopPrice": str(SL),
        "newClientOrderId": "SL",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)
    return cantidad_total


"############################"


def buy(SL, TP, porcentaje=0.9):
    params = {
        "symbol": "BTCUSDT",
    }

    response = BinanceAPI.send_signed_request("GET", "/fapi/v1/ticker/price", params)
    precio = float(response['price'])

    response = BinanceAPI.send_signed_request("GET", "/fapi/v2/balance")
    balance = float(response[1]['balance']) * porcentaje

    cantidad_total = balance / precio * 5
    cantidad_total = round(cantidad_total, 3)

    params = {
        "symbol": "BTCUSDT",
        "leverage": 5,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/leverage", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "marginType": "ISOLATED",
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/marginType", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "BUY",
        "type": "MARKET",
        "newClientOrderId": "Test1",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "TAKE_PROFIT_MARKET",
        "stopPrice": str(TP),
        "newClientOrderId": "TP",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

    params = {
        "symbol": "BTCUSDT",
        "side": "SELL",
        "type": "STOP_MARKET",
        "stopPrice": str(SL),
        "newClientOrderId": "SL",
        "quantity": 1,
    }

    response = BinanceAPI.send_signed_request("POST", "/fapi/v1/order", params)
    print(response)

sell(60000, 10000)
cancelAllOrders()
input("")
buy(10000, 60000)
input("")
cancelAllOrders()"""

"""cantidad = BinanceAPI.sell(150000, 2000)
input()
BinanceAPI.cancelAllOrders(cantidad, 0)"""

"""dmi_binance = np.array(
        [21.6499, 21.6349, 20.7740, 20.0176, 20.116, 17.9889, 17.2017, 16.1312, 15.4144, 15.0159, 18.1604, 18.6942,
         20.7908, 20.9799, 19.3777, 21.1631, 21.00, 19.9675, 21.3735, 21.17, 23.1167, 24.9497])
dmi_trading_view = np.array(
        [22.5, 22.7, 21.9, 21.0, 21.1, 18.8, 18.1, 17.0, 16.2, 15.8, 19.2, 19.6, 21.8, 21.9, 20.3, 22.4, 22.5, 21.4,
         23.1, 22.7, 25.2, 25.6], dtype=float)"""

import math

"""import numpy as np, pandas as pd
from numpy.core.records import ndarray
from pandas import DataFrame, Series


def SSLChannels(dataframe, length=10, mode="sma"):
    
    Source: https://www.tradingview.com/script/xzIoaIJC-SSL-channel/
    Author: xmatthias
    Pinescript Author: ErwinBeckers
    SSL Channels.
    Average over highs and lows form a channel - lines "flip" when close crosses
    either of the 2 lines.
    Trading ideas:
        * Channel cross
        * as confirmation based on up > down for long
    Usage:
        dataframe['sslDown'], dataframe['sslUp'] = SSLChannels(dataframe, 10)
    
    if mode not in "sma":
        raise ValueError(f"Mode {mode} not supported yet")

    df = dataframe.copy()

    if mode == "sma":
        df["smaHigh"] = df["high"].rolling(length).mean()
        df["smaLow"] = df["low"].rolling(length).mean()

    df["hlv"] = np.where(
        df["close"] > df["smaHigh"], 1, np.where(df["close"] < df["smaLow"], -1, np.NAN)
    )
    df["hlv"] = df["hlv"].ffill()

    df["sslDown"] = np.where(df["hlv"] < 0, df["smaHigh"], df["smaLow"])
    df["sslUp"] = np.where(df["hlv"] < 0, df["smaLow"], df["smaHigh"])

    return df["sslDown"], df["sslUp"]


BASE_URL = "https://api.binance.com"
r = requests.get(BASE_URL + '/api/v3/klines?symbol=BTCUSDT&interval=15m')
values = r.json()
values = json.dumps(values)
values = json.loads(values)
values = values[490:]
lows = []
highs = []
closes = []
for v in values:
    lows.append(float(v[3]))
    highs.append(float(v[2]))
    closes.append(float(v[4]))

dic = {'low': lows, 'high': highs, 'close': closes}
df = DataFrame.from_dict(dic)
print(df['low'])

down, high = SSLChannels(df, 10)
print(down)
print(high)"""



KEY = "9DMJuBctsl3xptp0BLZWFsgnkH9BGFsuJzgXknPRbc2Xj2ukNfYe34iaXYmrlT0H"
SECRET = "ERUzkv08WettczvQX7bZAsGK2I7qVFw2p8yHO0cXwux9Qg2UJ2pVoLWMNi8n7CY2"
BinanceAPI = BinanceAPI.BinanceAPI(KEY, SECRET)

response = BinanceAPI.send_signed_request("GET", "/fapi/v2/balance")
usdt = 0
for r in response:
    if r['asset'] == 'USDT':
        usdt = float(r['balance'])
print(response)
#balance = float(response[1]['balance']) * 0.9
print("Balance de la cuenta: " + str(usdt) + "\n")
























