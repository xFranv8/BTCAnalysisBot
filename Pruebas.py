import TelegramBot, datetime
from pytz import timezone

madrid = timezone('Europe/Madrid')

print(str(datetime.datetime.now(madrid)))