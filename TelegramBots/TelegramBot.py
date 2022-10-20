from bs4 import BeautifulSoup
import requests
import schedule

def send_message(message):
    token = ''
    chat_id = ''
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)
    return response


def BTCPrice():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text

    return format_result


def BTCFearAndGreedIndex():
    url = requests.get('https://alternative.me/crypto/fear-and-greed-index/')
    soup = BeautifulSoup(url.content, 'html.parser')
    result = soup.find('div', {'class': 'fng-circle'})
    format_result = result.text

    return format_result
