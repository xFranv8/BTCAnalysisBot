import numpy as np
import requests, datetime, BinanceAPI
import json
from pandas import DataFrame
from pytz import timezone
from time import sleep
from TelegramBots import GamblingBot

TOKEN_API = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZ2MzB2YXpxdWV6QGdtYWlsLmNvbSIsImlhdCI6MTY0NDQ5OTk0NywiZXhwIjo3OTUxNjk5OTQ3fQ.m3q94ib6HuFON7k99LCeT76USGCeLvy0K8dnj8dSHwQ"
KEY = "9DMJuBctsl3xptp0BLZWFsgnkH9BGFsuJzgXknPRbc2Xj2ukNfYe34iaXYmrlT0H"
SECRET = "ERUzkv08WettczvQX7bZAsGK2I7qVFw2p8yHO0cXwux9Qg2UJ2pVoLWMNi8n7CY2"
BINANCEAPI = BinanceAPI.BinanceAPI(KEY, SECRET)
COMPROBACION = False
OBJETIVO = -1
ACUMULADO = 0
MADRID = timezone('Europe/Madrid')

def SSLChannels(length=10, mode="sma"):
    """ Source: https://www.tradingview.com/script/xzIoaIJC-SSL-channel/
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
     """

    values = BINANCEAPI.get_klines(10)
    lows = []
    highs = []
    closes = []
    for v in values:
        lows.append(float(v[3]))
        highs.append(float(v[2]))
        closes.append(float(v[4]))

    dic = {'low': lows, 'high': highs, 'close': closes}
    dataframe = DataFrame.from_dict(dic)

    if mode in "sma":
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
        # Down -> Rojo  Up -> Verde
        return df["sslDown"][9], df["sslUp"][9]

    raise ValueError(f"Mode {mode} not supported yet")


def compare_ema():
    r = requests.get(
        'https://api.taapi.io/ema?secret=' + TOKEN_API + '&exchange=binance&symbol=BTC/USDT&interval=5m'
                                                         '&optInTimePeriod=200')

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return False, -1

    values = r.json()
    # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
    values = json.dumps(values)
    values = json.loads(values)
    price = BINANCEAPI.get_ticker_price()
    ema = float(values['value'])
    if price > ema:
        # Compras
        return 1
    elif price == ema:
        # Nada
        return -1
    else:
        # Ventas
        return 0


def strategy():
    global COMPROBACION, OBJETIVO
    madrid = timezone('Europe/Madrid')
    minutos = datetime.datetime.now(madrid).minute
    if minutos % 5 == 4:
        if not COMPROBACION:
            OBJETIVO = compare_ema()
            sleep(40)
            COMPROBACION = True
            with open("SSLData/data.json", 'r') as f:
                values = json.load(f)
                length = len(values)
                ssl_vela_formandose = values[length - 1]
                ssl_vela_anterior = values[length - 2]
            print()
            print()
            print("Estamos en: ", OBJETIVO)
            print("SSL vela formandose: ", ssl_vela_formandose["green"], " - VERDE, ", ssl_vela_formandose["red"],
                  " - ROJO\n")
            print("SSL vela anterior:  ", ssl_vela_anterior["green"], "  - VERDE, ", ssl_vela_anterior["red"],
                  "- ROJO\n")
            if OBJETIVO == 1:
                if ssl_vela_anterior["green"] < ssl_vela_anterior["red"] and ssl_vela_formandose["green"] > \
                        ssl_vela_formandose["red"]:
                    print("ALERTA EN COMPRAS")
                    message = "[EMPEZAMOS OPERACION DE COMPRAS] " + "\U000023F3"
                    GamblingBot.send_message(message)
                    return True, ssl_vela_formandose["red"] - 2, 1
                else:
                    print("NO HAY CRUCE EN COMPRAS")
                    return False, 0, OBJETIVO
            elif OBJETIVO == 0:
                if ssl_vela_anterior["red"] < ssl_vela_anterior["green"] and ssl_vela_formandose["red"] > \
                        ssl_vela_formandose["green"]:
                    print("ALERTA EN VENTAS")
                    message = "[EMPEZAMOS OPERACION DE VENTAS] " + "\U000023F3"
                    GamblingBot.send_message(message)
                    return True, ssl_vela_formandose["red"] + 2, 0
                else:
                    print("NO HAY CRUCE EN VENTAS")
                    return False, 0, OBJETIVO
            else:
                return False, 0, -1
        else:
            return False, 0, -1
    else:
        COMPROBACION = False
        return False, 0, -1


def stop_position(open_price, SL, objetivo, ):
    global ACUMULADO
    porcentaje_SL = 100 - ((SL * 100) / open_price)
    exit = False
    sleep(30)
    last_line = BINANCEAPI.get_klines(1)

    with open("SSLData/data.json", 'r') as f:
        values = json.load(f)
        length = len(values)
        ssl_current_kline = values[length - 1]
        ssl_last_kline = values[length - 2]

    if objetivo == 1:
        # En este caso el High es superior o igual al TP, por lo que habriamos ganado.
        if ssl_last_kline["red"] < ssl_last_kline["green"] and ssl_current_kline["red"] > ssl_current_kline["green"]:
            price = BINANCEAPI.get_ticker_price()
            if open_price < price:
                porcentaje_TP = ((price * 100) / open_price) - 100
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP)
                exit = True
                print(message)
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP)
                ACUMULADO = ACUMULADO + float(porcentaje_TP)
                GamblingBot.send_message(message)
        # En este caso el Low es inferior o igual al SL por lo que hubieramos perdido.
        elif float(last_line[1][0][3]) <= SL:
            message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(-porcentaje_SL)
            exit = True
            print(message)
            message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(porcentaje_SL)
            ACUMULADO = ACUMULADO - float(porcentaje_SL)
            GamblingBot.send_message(message)
    # Si estamos aqui es porque objetivo es igual a 0 lo que significa que estamos en ventas y es al reves.
    else:
        # En este caso el Low es inferior o igual al TP profit por lo que hubieramos ganado.
        if ssl_last_kline["green"] < ssl_last_kline["red"] and ssl_current_kline["green"] > ssl_current_kline["red"]:
            price = BINANCEAPI.get_ticker_price()
            if open_price > price:
                porcentaje_TP = ((price * 100) / open_price) - 100
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP * -1)
                exit = True
                print(message)
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP * -1)
                ACUMULADO = ACUMULADO + float(-porcentaje_TP)
                GamblingBot.send_message(message)
        # En este caso el High es superior o igual al SL por lo que hubieramos perdido
        elif float(last_line[1][0][2]) >= SL:
            message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(porcentaje_SL)
            exit = True
            print(message)
            message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(porcentaje_SL)
            ACUMULADO = ACUMULADO + float(porcentaje_SL)
            GamblingBot.send_message(message)
    return exit


while True:
    operamos = strategy()

    if operamos[0]:
        SL = float(operamos[1])
        open_price = BINANCEAPI.get_ticker_price()
        message = "Empezamos operación de " + str(OBJETIVO) + " con fecha: " + str(datetime.datetime.now(MADRID)) + '\n' + \
                  "Precio de apertura de la operación: " + str(open_price) + '\n' + \
                  "STOP LOSS: " + str(SL) + '\n'
        GamblingBot.send_message(message)
        opened_position = False
        while not opened_position:
            opened_position = stop_position(open_price, SL, operamos[2])
