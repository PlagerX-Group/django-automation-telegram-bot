from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton("Запуск автотестов"),
            InlineKeyboardButton("История запуска автотестов"),
        ]
    ]

    return InlineKeyboardMarkup(buttons)
