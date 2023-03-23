from telegram import Update
from telegram.ext import CallbackContext
from telegrambot.utils.decorators import only_exists_user


@only_exists_user
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='*Добро пожаловать в Telegram-бота для автоматизации тестирования!*\n\n'
        f'*Пользователь:* {" ".join([update.effective_user.first_name, update.effective_user.last_name])}\n'
        f'*ID:* {update.effective_user.id}'
    )
