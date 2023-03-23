import typing as t

from telegram import Update
from telegram.ext import CallbackContext
from telegramusers.models import TelegramUserModel


def only_exists_user(func: t.Callable) -> t.Callable[[...], t.Optional[t.Any]]:
    def wrapper(update: Update, context: CallbackContext) -> t.Optional[t.Any]:
        if TelegramUserModel.get_user(update, context) is not None:
            return func(update, context)
        else:
            update.message.reply_text("Пользователь не идентифицирован")
            return
    return wrapper
