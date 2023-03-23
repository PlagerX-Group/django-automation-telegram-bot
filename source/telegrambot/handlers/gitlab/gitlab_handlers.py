import enum

from django.shortcuts import get_object_or_404
from gitlab.models import GitlabRepositoryModel
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
)
from telegrambot.utils.decorators import only_exists_user


@enum.unique
class PipelineStatusEnum(enum.Enum):
    NOT_STARTED: str = "Не запущен"
    STARTED: str = "Запущен"
    CANCELLED: str = "Отменен"
    PASSED: str = "Пройден"
    FAILED: str = "Завершен с ошибками"


@enum.unique
class ConversationStatesEnum(enum.Enum):
    SERVICE_INFORMATION = 1
    PIPELINE_IS_CONFIRMED = 10
    PIPELINE_RUN_YES = 11
    PIPELINE_RUN_NO = 12

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()


def generate_pipeline_template(repo_id: int, pipeline_status: PipelineStatusEnum, /) -> str:

    # Поиск репозитория.
    repository: GitlabRepositoryModel = get_object_or_404(GitlabRepositoryModel, pk=repo_id)

    kwargs = {
        'reponame': repository.repo_name,
        'repodescription': repository.description,
        'repotargetref': repository.target_ref,
        'pipelinestatus': pipeline_status.value,
    }
    return (
        "*Подготовка к запуску автотестов*\n\n"
        "*Проект:* {reponame}\n"
        "*Описание проекта:* {repodescription}\n"
        "*Ветка*: {repotargetref}\n"
        "*Статус пайплайна:* {pipelinestatus}"
    ).format(**kwargs)


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
            "Выберите автотесты для запуска:",
            reply_markup=keyboard,
        )
    else:
        update.message.reply_text("Отсутствуют автотесты для запуска")


@only_exists_user
def gitlab_show_service_information(update: Update, context: CallbackContext):

    # Получаем callback ответ.
    query = update.callback_query
    query.answer()
    data = query.data

    # ID репозитория
    repo_id = int(data.rsplit('-', maxsplit=1)[-1])

    # Записываем ID репозитория.
    context.user_data['run-repository-id'] = repo_id

    # Отправка сообщения.
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Запустить пайплайн", callback_data=str(ConversationStatesEnum.PIPELINE_RUN_YES)),
                InlineKeyboardButton("Отменить", callback_data=str(ConversationStatesEnum.PIPELINE_RUN_NO)),
            ]
        ]
    )
    query.edit_message_text(
        generate_pipeline_template(repo_id, PipelineStatusEnum.NOT_STARTED),
        reply_markup=keyboard,
    )
    return ConversationStatesEnum.PIPELINE_IS_CONFIRMED


@only_exists_user
def gitlab_confirm_run_pipeline(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # ID репозитория
    repo_id = context.user_data['run-repository-id']

    buttons = [
        [InlineKeyboardButton("Отменить запуск пайплайна", callback_data=str(ConversationStatesEnum.PIPELINE_RUN_NO))]
    ]

    query.edit_message_text(
        generate_pipeline_template(repo_id, PipelineStatusEnum.STARTED), reply_markup=InlineKeyboardMarkup(buttons)
    )

    return ConversationStatesEnum.PIPELINE_IS_CONFIRMED


@only_exists_user
def gitlab_cancel_run_pipeline(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # ID репозитория
    repo_id = context.user_data['run-repository-id']

    query.edit_message_text(generate_pipeline_template(repo_id, PipelineStatusEnum.CANCELLED))
    return ConversationHandler.END


def gitlab_conversation_handler():
    conv_handler = ConversationHandler(
        name="gitlab_conversation",
        entry_points=[CallbackQueryHandler(gitlab_show_service_information)],
        states={
            ConversationStatesEnum.PIPELINE_IS_CONFIRMED: [
                CallbackQueryHandler(
                    gitlab_confirm_run_pipeline, pattern="^" + str(ConversationStatesEnum.PIPELINE_RUN_YES) + "$"
                ),
                CallbackQueryHandler(
                    gitlab_cancel_run_pipeline, pattern='^' + str(ConversationStatesEnum.PIPELINE_RUN_NO) + '$'
                ),
            ]
        },
        fallbacks=[],
        per_message=True,
    )
    return conv_handler
