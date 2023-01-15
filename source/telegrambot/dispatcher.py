# from django.conf import settings
from django.conf import settings
from telegram.ext import CommandHandler, Dispatcher
from telegrambot.handlers.admin import handlers as admin_handlers
from telegrambot.handlers.onboarding import handlers as onboarding_handlers
from telegrambot.main import telegram_bot


# from telegrambot.main import telegram_bot


def setup_dispatcher(dispatch):
    dispatch.add_handler(CommandHandler('start', onboarding_handlers.command_start))
    dispatch.add_handler(CommandHandler('admin', admin_handlers.admin))
    return dispatch


if settings.DEBUG:
    kwargs = {
        'workers': 0,
        'update_queue': None,
    }
else:
    kwargs = {
        'workers': 4,
        'update_queue': None,
    }
dispatcher = setup_dispatcher(Dispatcher(telegram_bot, **kwargs))
