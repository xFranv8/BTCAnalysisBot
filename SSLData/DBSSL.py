import numpy as np
import requests, datetime, TelegramBot, BinanceAPI
import json
from pandas import DataFrame
from pytz import timezone
from time import sleep
from pyfiglet import Figlet

PATH = "data.json"


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

    BASE_URL = "https://api.binance.com"
    r = requests.get(BASE_URL + '/api/v3/klines?symbol=BTCUSDT&interval=5m')
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


def append_to_json(data, PATH):
    with open(PATH, 'ab+') as f:
        f.seek(0, 2)  # Go to the end of file
        if f.tell() == 0:  # Check if file is empty
            f.write(json.dumps([data]).encode())  # If empty, write an array
        else:
            f.seek(-1, 2)
            f.truncate()  # Remove the last character, open the array
            f.write(' , '.encode())  # Write the separator
            f.write(json.dumps(data).encode())  # Dump the dictionary
            f.write(']'.encode())  # Close the array


def delete_json(values):
    firstData = values
    firstData.pop(0)
    with open(PATH, 'w') as f:
        f.write(json.dumps(firstData))


aux = False
while True:
    madrid = timezone('Europe/Madrid')
    minutos = datetime.datetime.now(madrid).minute

    if minutos % 5 == 0:
        if not aux:
            (red, green) = SSLChannels()
            data = {
                'red': red,
                'green': green
            }
            print("Writing values to file")
            append_to_json(data, PATH)
            with open(PATH, 'r+') as f:
                values = json.load(f)
            if len(values) == 3:
                delete_json(values)
                print(values[len(values) - 1])
            aux = True
    else:
        aux = False
