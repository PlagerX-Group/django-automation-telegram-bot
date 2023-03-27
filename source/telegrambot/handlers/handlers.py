from telegram import Update
from telegram.ext import CallbackContext

from telegrambot.utils.decorators import only_exists_user
from telegrambot.utils.validators import Validator, ValidatorErrorsEnum, ValidatorWarningsEnum


@only_exists_user
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='<b>Добро пожаловать в Telegram-бота для автоматизации тестирования!</b>\n\n'
        f'<b>Пользователь:</b> {" ".join([update.effective_user.first_name, update.effective_user.last_name])}\n'
        f'<b>ID:</b> {update.effective_user.id}'
    )


@only_exists_user
def validateusersettigs(update: Update, context: CallbackContext):

    # Ошибки для вывода
    errors: list[ValidatorErrorsEnum] = [
        Validator.validate_user_gitlab(update.effective_user.id)
    ]

    # Удаляем все None
    errors = list(
        filter(lambda x: x not in [ValidatorWarningsEnum.CORRECT, ValidatorErrorsEnum.CORRECT], errors)
    )

    # Удаляем старое сообщение
    chat_id = update.message.chat_id
    message_id = update.message.message_id
    context.bot.delete_message(chat_id, message_id)

    # Выводим сообщение
    if errors:
        error_text = ""
        warns_text = ""
        error_nums = 0
        warns_nums = 0

        for error in errors:
            if isinstance(error, ValidatorWarningsEnum):
                warns_nums += 1
                warns_text += f"{warns_nums}) {error.value}\n"
            elif isinstance(error, ValidatorErrorsEnum):
                error_nums += 1
                error_text += f"{error_nums}) {error.value}\n"

        if error_text != "":
            error_text = f"<b>Найдены ошибки у пользователя:</b>\n{error_text}\n\n"
        if warns_text != "":
            warns_text = f"<b>Найдены предупреждения у пользователя:</b>\n{warns_text}"

        update.message.reply_text(error_text + warns_text)
    else:
        update.message.reply_text('Настройки пользователя корректно настроены!')
