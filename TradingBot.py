from time import sleep
from pyfiglet import Figlet
import requests, datetime, TelegramBot, BinanceAPI
import json
from pytz import timezone

# Constante con el Token de la API para obtener el valor de los indicadores.
TOKEN_API_INDICATORS = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM"
testnet = "https://testnet.binancefuture.com"
# Claves DanielMegaRabón para testear
KEY_D = "b94b3f278f28a791d7764ea0bebb38f5a73dea4e4fec7eb6cf367103eafa0bcb"
SECRET_D = "40916e9b070693fd166cbab6222c58d0290b65433ae1942aa151d44d953b258a"
BinanceAPI = BinanceAPI.BinanceAPI(KEY_D, SECRET_D)


def getDMI(objetivo):
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get(
        'https://api.taapi.io/dmi?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&backtracks=2')
    values = r.json()

    # Compruebo si existe algun problema al realizar la peticion.
    if r.status_code != 200:
        return (False, -1)
    else:
        # Convierto la variable que posee los valores en JSON para que puedan ser utilizados con python de manera sencilla
        values = json.dumps(values)
        values = json.loads(values)
        lista_dmis = []

        for v in values:
            if objetivo == -1:
                return [False, -1]
            elif objetivo == 0:
                lista_dmis.append(float(v["minusdi"]))
            elif objetivo == 1:
                lista_dmis.append(float(v["plusdi"]))
        return (True, lista_dmis)


def getMA50():
    # Peticion GET al endpoint de la API que devuelve los valores de los indicadores.
    # Seria muy interesante obtener el ADX y el resto de valores de Binance Futuros USDM. https://api.taapi.io/dmi?secret=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InJvYWR0bzFtaWxsaW9uMjAyNkBnbWFpbC5jb20iLCJpYXQiOjE2NDMxMTE4NTgsImV4cCI6Nzk1MDMxMTg1OH0.GmJoKq_wyWfAhkfBA0jJp7kCELHCZVfycDYvexbRytM&exchange=binanceusdm&symbol=BTC/USDT&interval=15m
    r = requests.get(
        'https://api.taapi.io/ma?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&optInTimePeriod=50')
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
    r = requests.get(
        'https://api.taapi.io/ma?secret=' + TOKEN_API_INDICATORS + '&exchange=binance&symbol=BTC/USDT&interval=15m&optInTimePeriod=200')
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

    sleep(15)

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
    take_profit = ((100 - porcentaje_TP) / 100) * open_price
    return take_profit


def result(stop_loss, take_profit, open_price, objetivo, acumulado):
    # Calculo los % para mostrarlos luego segun el open price, el stop_loss y el take_profit
    porcentaje_SL = 100 - ((stop_loss * 100) / open_price)
    porcentaje_TP = ((take_profit * 100) / open_price) - 100

    # Seteo una variable booleana a False para que hasta que no se haya terminado la operacion siga monitorizando si toca TP o SL.
    exito = False

    while not exito:
        sleep(30)
        # Obtengo la ultima vela que se ha formado constantemente hasta que el High o el Low superen al SL o al TP.
        last_line = BinanceAPI.get_klines(1)

        # Si estamos en compras el High debe ser superior al TP para ganar o el Low debe ser inferior al SL para perder.
        if objetivo == 1:
            # En este caso el High es superior o igual al TP, por lo que habriamos ganado.
            if float(last_line[1][0][2]) >= take_profit:
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP)
                acumulado[0] = acumulado[0] + float(porcentaje_TP)
                TelegramBot.send_message(message)
                exito = True
            # En este caso el Low es inferior o igual al SL por lo que hubieramos perdido.
            elif float(last_line[1][0][3]) <= stop_loss:
                message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(-porcentaje_SL)
                acumulado[0] = acumulado[0] - float(porcentaje_SL)
                TelegramBot.send_message(message)
                exito = True
        # Si estamos aqui es porque objetivo es igual a 0 lo que significa que estamos en ventas y es al reves.
        else:
            # En este caso el Low es inferior o igual al TP profit por lo que hubieramos ganado.
            if float(last_line[1][0][3]) <= take_profit:
                message = "Operacion ganada" + "\U0001F680" + "!!!\n" + "% Realizado: " + str(porcentaje_TP*-1)
                acumulado[0] = acumulado[0] + float(porcentaje_TP*-1)
                TelegramBot.send_message(message)
                exito = True
            # En este caso el High es superior o igual al SL por lo que hubieramos perdido
            elif float(last_line[1][0][2]) >= stop_loss:
                message = "Operacion perdida" + "\U0001F921" + "!!!\n" + "% Realizado: " + str(porcentaje_SL)
                acumulado[0] = acumulado[0] + float(porcentaje_SL)
                TelegramBot.send_message(message)
                exito = True
    message = "% Acumulado: " + str(acumulado[0]) + "\U0001F3A2"
    return message


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
imprimir = True

while True:
    madrid = timezone('Europe/Madrid')
    minutos = datetime.datetime.now(madrid).minute

    # Comprobamos la posicion de las dos medias a las horas correspondientes.
    if (minutos == 13) or (minutos == 28) or (minutos == 43) or (minutos == 58):
        # -1 Medias Iguales, no hacemos nada
        # 0 Buscamos ventas
        # 1 Buscamos compras.
        if not medias_comprobadas:
            objetivo = compararMedias()
            medias_comprobadas = True

    if (minutos == 14) or (minutos == 29) or (minutos == 44) or (minutos == 59) and objetivo != -1:
        if not saved_adx:
            lista_DMI = getDMI(objetivo)[1]
            saved_adx = True
        if lista_DMI[0] > 25.00 > lista_DMI[1] and objetivo != -1:
            operamos = True

            if imprimir:
                print("")
                print("[EMPEZAMOS OPERACION]\n")
                print("Fecha: " + str(datetime.datetime.now(madrid)))
                print("Objetivo: " + str(objetivo))
                print("DI de la vela actual: " + str(lista_DMI[0]))
                print("DI de la vela anterior: " + str(lista_DMI[1]))
                print("[ESPERANDO AL FIN DEL CUARTO DE HORA PARA LANZAR LA ORDEN]")
                print("")

                message = "[EMPEZAMOS OPERACION] " + "\U000023F3"
                TelegramBot.send_message(message)
                imprimir = False

    if (minutos == 15) or (minutos == 30) or (minutos == 45) or (minutos == 00):
        if operamos and not BinanceAPI.existsOpenOrders():
            last_klines = BinanceAPI.get_klines(15)
            open_price = float(last_klines[1][14][4])
            aux = []
            if objetivo == 1:
                # Estamos en compras
                for kline in last_klines[1]:
                    aux.append(kline[3])
                stop_loss = float(calc_stop_loss_buys(aux))
                take_profit = calc_take_profit(stop_loss, open_price)

                print("")
                print("[DATOS DE LA ORDEN DE COMPRA]")
                print("Fecha: " + str(datetime.datetime.now(madrid)))
                print("Precio de apertura: " + str(open_price))
                print("Stop Loss: " + str(stop_loss))
                print("Take Profit: " + str(take_profit))
                print("")

                cantidad_orden_contraria = BinanceAPI.buy(stop_loss, take_profit)
                type = "COMPRA"
            else:
                # Estamos en ventas
                for kline in last_klines[1]:
                    aux.append(kline[2])
                stop_loss = float(calc_stop_loss_sells(aux))
                take_profit = calc_take_profit(stop_loss, open_price)

                print("")
                print("[DATOS DE LA ORDEN DE VENTA]")
                print("Fecha: " + str(datetime.datetime.now(madrid)))
                print("Precio de apertura: " + str(open_price))
                print("Stop Loss: " + str(stop_loss))
                print("Take Profit: " + str(take_profit))
                print("")

                cantidad_orden_contraria = BinanceAPI.sell(stop_loss, take_profit)
                type = "VENTA"

            message = "Empezamos operación de " + type + " con fecha: " + str(datetime.datetime.now(madrid)) + '\n' + \
                      "Precio de apertura de la operación: " + str(open_price) + '\n' + \
                      "STOP LOSS: " + str(stop_loss) + '\n' + \
                      "TAKE PROFIT: " + str(take_profit)
            TelegramBot.send_message(message)
            operamos = False

            # Tener en cuenta que probablemente haya que cerrar las operaciones manualmente desde la testnet con la
            # cuenta de daniel ya que no se cierran por defecto porque estamos cogiendo datos con otros precios
            while BinanceAPI.existsOpenOrders():
                respuesta = result(stop_loss, take_profit, open_price, objetivo, [0])
                BinanceAPI.cancelAllOrders(cantidad_orden_contraria, objetivo)
            TelegramBot.send_message(respuesta)

        saved_adx = False
        medias_comprobadas = False
        imprimir = True
