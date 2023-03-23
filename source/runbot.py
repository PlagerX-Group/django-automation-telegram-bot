import os

import django
import pytz
from django.conf import settings
from telegram import ParseMode
from telegram.ext import Defaults, Updater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()


def run_bot():
    from telegrambot.dispatcher import setup_dispatcher

    defaults = Defaults(parse_mode=ParseMode.MARKDOWN, tzinfo=pytz.timezone('Europe/Moscow'))
    updater = Updater(settings.TELEGRAM_BOT_ACCESS_TOKEN, defaults=defaults)
    setup_dispatcher(updater.dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
