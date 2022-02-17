import requests


def send_message(bot_message):
    bot_token = '5272685092:AAGkFf4cpuCBJfcMz_layY-5uv1kOZytZgA'
    bot_chatID = '-605534118'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response
