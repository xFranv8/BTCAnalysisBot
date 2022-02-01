import datetime, BinanceAPI
from time import sleep

from pytz import timezone
from pyfiglet import Figlet

import TelegramBot


def banner():
    custom_fig = Figlet(font='big')
    print(custom_fig.renderText('BTC Trading Bot'))
    print("Bot inicializado ....")


banner()
operamos = False
medias_comprobadas = False
saved_adx = False
pruebas = False
acumulado = [0]
objetivo = -1

BinanceAPI = BinanceAPI.BinanceAPI("b94b3f278f28a791d7764ea0bebb38f5a73dea4e4fec7eb6cf367103eafa0bcb",
                                   "40916e9b070693fd166cbab6222c58d0290b65433ae1942aa151d44d953b258a")

def calc_take_profit(SL, open_price):
    # open_price = get_klines(1)[1][1]
    porcentaje_TP = (((SL * 100) / open_price) - 100) / 2
    take_profit = ((100 - porcentaje_TP) / 100) * open_price
    return take_profit


def compararMedias():
    return 1


def result(stop_loss, take_profit, open_price, objetivo, acumulado):
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
    TelegramBot.send_message(message)


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

    if operamos:  # and not BinanceAPI.existsOpenOrders():
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

cantidad = BinanceAPI.sell(150000, 2000)
input()
BinanceAPI.cancelAllOrders(cantidad, 0)