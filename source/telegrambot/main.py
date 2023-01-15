import telegram
from django.conf import settings
from telegram import Bot

try:
    telegram_bot = Bot(settings.TELEGRAM_BOT_ACCESS_TOKEN)
except telegram.error.Unauthorized as exc:
    raise telegram.error.Unauthorized('Incorrect TELEGRAM_BOT_ACCESS_TOKEN') from exc
