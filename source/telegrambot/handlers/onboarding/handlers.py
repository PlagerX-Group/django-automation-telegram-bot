from telegram import Update
from telegram.ext import CallbackContext
from telegrambot.handlers.onboarding import static_text
from telegrambot.handlers.onboarding.keyboards import make_keyboard_for_start_command
from telegramusers.models import TelegramUserModel


def command_start(update: Update, context: CallbackContext) -> None:
    user: TelegramUserModel = TelegramUserModel.get_user(update, context)

    if user:
        text = static_text.start_created.format(first_name=user.user.username)
    else:
        text = "dsdasdsadasdsa"
    update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())
