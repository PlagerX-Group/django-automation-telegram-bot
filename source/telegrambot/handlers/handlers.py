from telegram import Update
from telegram.ext import CallbackContext
from telegrambot.utils.decorators import only_exists_user


@only_exists_user
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='<b>Добро пожаловать в Telegram-бота для автоматизации тестирования!</b>\n\n'
        f'<b>Пользователь:</b> {" ".join([update.effective_user.first_name, update.effective_user.last_name])}\n'
        f'<b>ID:</b> {update.effective_user.id}'
    )
