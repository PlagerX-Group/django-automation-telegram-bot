import os
import django

from django.conf import settings
from telegram.ext import Updater

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()


def run_bot():
    from telegrambot.dispatcher import setup_dispatcher

    token_bot = settings.TELEGRAM_BOT_ACCESS_TOKEN
    updater = Updater(token_bot)
    setup_dispatcher(updater.dispatcher)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run_bot()
