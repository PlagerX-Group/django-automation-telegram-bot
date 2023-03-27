import typing as t

from telegram import Update
from telegram.ext import CallbackContext
from extendeduser.models import ExtendedUserModel


def only_exists_user(func: t.Callable) -> t.Callable[[...], t.Optional[t.Any]]:
    def wrapper(update: Update, context: CallbackContext) -> t.Optional[t.Any]:
        if ExtendedUserModel.get_telegram_user(update, context) is not None:
            return func(update, context)
        else:
            update.message.reply_text(f"Пользователь не идентифицирован (user-id={update.effective_user.id})")
            return

    return wrapper
