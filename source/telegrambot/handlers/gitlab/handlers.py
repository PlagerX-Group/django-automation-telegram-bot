from django.shortcuts import get_object_or_404
from gitlab.models import GitlabRepositoryModel
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Dispatcher, CallbackContext,
)
from telegrambot.utils.decorators import only_exists_user

SHOW_SERVICE_INFORMATION = 0
PIPELINE_IS_CONFIRMED = 10
PIPELINE_RUN_YES = 11
PIPELINE_RUN_NO = 12


@only_exists_user
def gitlab_show_services(update: Update, context: CallbackContext) -> None:

    if repositories := GitlabRepositoryModel.objects.filter(is_active=True).all():
        buttons = [[]]
        row_num = -1
        for index, repository in enumerate(repositories):
            repository: GitlabRepositoryModel = repository
            if index % 2 == 0:
                row_num += 1
                buttons.append([])
            buttons[row_num].append(
                InlineKeyboardButton(repository.repo_name, callback_data=f'run-gitlab-{repository.id}')
            )
        keyboard = InlineKeyboardMarkup(buttons)
        update.message.reply_text(
            "Выберите автотесты для запуска.\n"
            "Для отмены используйте команду /cancel",
            reply_markup=keyboard,
        )
        return SHOW_SERVICE_INFORMATION
    else:
        update.message.reply_text("Отсутствуют автотесты для запуска")
        return ConversationHandler.END


@only_exists_user
def gitlab_show_service_information(update: Update, context: CallbackContext):

    # Получаем callback ответ.
    query = update.callback_query
    query.answer()
    data = query.data

    # ID репозитория
    repo_id = int(data.rsplit('-', maxsplit=1)[-1])

    # Поиск репозитория.
    repository: GitlabRepositoryModel = get_object_or_404(GitlabRepositoryModel, pk=repo_id)

    # Отправка сообщения.
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Запустить пайплайн", callback_data=str(PIPELINE_RUN_YES)),
                InlineKeyboardButton("Отменить", callback_data=str(PIPELINE_RUN_NO))
            ]
        ]
    )
    query.edit_message_text(
        text=f"*Запуск автотестов для проекта:* {repository.repo_name}\n"
             f"*Описание проекта:* {repository.description}\n"
             f"*Ветка*: {repository.target_ref}\n"
            f"*URL триггера*: {repository.repo_link}",
        parse_mode='markdown',
        reply_markup=keyboard,
    )

    return PIPELINE_IS_CONFIRMED


@only_exists_user
def gitlab_confirmation_pipeline(update: Update, context: CallbackContext):

    if update.message.text == str(PIPELINE_RUN_YES):
        pass
    elif update.message.text == str(PIPELINE_RUN_NO):
        update.message.reply_text('Запуск пайплайна отменен!')

    return ConversationHandler.END


@only_exists_user
def gitlab_cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Действие с Gitlab отменено!')
    return ConversationHandler.END


def gitlab_conversation_handler():
    conv_handler = ConversationHandler(
        name="gitlab_conversation",
        entry_points=[CommandHandler('gitlab', gitlab_show_services)],
        states={
            SHOW_SERVICE_INFORMATION: [CallbackQueryHandler(gitlab_show_service_information)],
            PIPELINE_IS_CONFIRMED: [CallbackQueryHandler(gitlab_confirmation_pipeline, pattern="^" + str(PIPELINE_IS_CONFIRMED) + "$")]
        },
        fallbacks=[CommandHandler('cancel', gitlab_cancel)],
    )
    return conv_handler


def registration_gitlab_handlers(dispatch: Dispatcher):
    dispatch.add_handler(gitlab_conversation_handler())

