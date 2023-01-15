from telegram import Update
from telegram.ext import CallbackContext
from telegramusers.models import TelegramUserModel


def admin(update: Update, context: CallbackContext) -> None:
    user = TelegramUserModel.get_user(update, context)
    if not user.is_staff:
        update.message.reply_text("ADMIN")
        return
    update.message.reply_text("ADMIN CMD")
