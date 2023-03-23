from telegram.ext import Dispatcher, CommandHandler
from .gitlab_handlers import gitlab_conversation_handler, gitlab_show_services


def registration_gitlab_handlers(dispatch: Dispatcher) -> None:
    dispatch.add_handler(CommandHandler('gitlab', gitlab_show_services))
    dispatch.add_handler(gitlab_conversation_handler())
