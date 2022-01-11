from bs4 import BeautifulSoup
import requests
import schedule

def send_message (message):
    token = '5025769377:AAEfXFMGYSnjnvv5465awVjmDpHt2WGdf30'
    chat_id = '-693670129'
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    return response


def send_BtcPrice ():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text

    return format_result


def send_BtcFearAndGreedIndex ():
    url = requests.get('https://alternative.me/crypto/fear-and-greed-index/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('div', {'class': 'fng-circle'})
    format_result = result.text

    return format_result


mensaje = "Buenos días, este es el resumen del día.\n" \
          "El precio del Bitcoin a dia de hoy es de : " + send_BtcPrice() + '\n' \
          "El valor de Fear and Greed Index es de: " + send_BtcFearAndGreedIndex()

test_bot = send_message(mensaje)