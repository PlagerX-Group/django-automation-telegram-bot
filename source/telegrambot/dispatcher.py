from django.conf import settings
from telegram import Bot, BotCommand
from telegram.ext import CommandHandler, Dispatcher
from telegrambot import telegram_bot
from telegrambot.handlers import handlers as general_handlers
from telegrambot.handlers.gitlab import registration_gitlab_handlers


if settings.DEBUG:
    dispatcher_kwargs = {
        'workers': 1,
        'update_queue': None,
    }
else:
    dispatcher_kwargs = {
        'workers': 4,
        'update_queue': None,
    }

setup_commands = {
    'start': 'Начало работы с ботом',
    'projectlist': 'Список проектов для запуска автотестов',
    'gitlabhistory': 'История запуска пайплайнов в Gitlab',
}


def setup_dispatcher(dispatch: Dispatcher):
    registration_gitlab_handlers(dispatch)
    dispatch.add_handler(CommandHandler('start', general_handlers.start))
    return dispatch


def setup_bot_commands(bot_instance: Bot, commands: dict, /) -> None:
    telegram_bot.delete_my_commands()
    bot_instance.set_my_commands([BotCommand(command, description) for command, description in commands.items()])


setup_bot_commands(telegram_bot, setup_commands)
dispatcher = setup_dispatcher(Dispatcher(telegram_bot, **dispatcher_kwargs))
