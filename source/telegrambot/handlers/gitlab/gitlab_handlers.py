import enum

from gitlab import Gitlab
from gitlab.exceptions import GitlabAuthenticationError, GitlabGetError, GitlabError
from django.shortcuts import get_object_or_404

from gitlabapp.models import (
    GitlabRepositoryRunsModel,
    GitlabRepositoryTokensModel,
    GitlabRepositoryPipelineModel,
    GitlabRepositoryPipelineHistoryModel,
)
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
    NOT_STARTED_WITH_ERRORS: str = "Ошибка при запуске"
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


def generate_pipeline_template(
    repo_id: int, pipeline_status: PipelineStatusEnum, /, reason: str = None,
) -> str:

    # Поиск рана.
    run: GitlabRepositoryRunsModel = get_object_or_404(GitlabRepositoryRunsModel, pk=repo_id)

    kwargs = {
        'reponame': run.name,
        'repodescription': run.description,
        'repotargetref': run.ref,
        'pipelinestatus': pipeline_status.value,
        'warnmsg': '',
    }

    template = (
        "<b>Подготовка к запуску автотестов</b>\n\n"
        "{warnmsg}"
        "<b>Проект:</b> {reponame}\n"
        "<b>Описание проекта:</b> {repodescription}\n"
        "<b>Ветка</b>: {repotargetref}\n"
        "<b>Статус пайплайна:</b> {pipelinestatus}"
    )
    if isinstance(run.warning_message,  str) and len(run.warning_message) > 0:
        kwargs['warnmsg'] = f"<b><code>{run.warning_message}</code></b>\n\n\n"

    if isinstance(reason, str):
        kwargs.update({'pipereason': reason})
        template += "\n<b>Причина:</b> {pipereason}"

    return template.format(**kwargs)


@only_exists_user
def gitlab_show_services(update: Update, context: CallbackContext) -> None:
    if runs := GitlabRepositoryRunsModel.objects.filter(is_active=True).all():
        buttons = [[]]
        row_num = -1
        for index, run in enumerate(runs):
            run: GitlabRepositoryRunsModel = run
            if index % 2 == 0:
                row_num += 1
                buttons.append([])
            buttons[row_num].append(
                InlineKeyboardButton(run.name, callback_data=f'run-gitlab-{run.id}')
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
    run_id = int(data.rsplit('-', maxsplit=1)[-1])

    # Записываем ID репозитория.
    context.user_data['run-repository-id'] = run_id

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
        generate_pipeline_template(run_id, PipelineStatusEnum.NOT_STARTED),
        reply_markup=keyboard,
    )
    return ConversationStatesEnum.PIPELINE_IS_CONFIRMED


@only_exists_user
def gitlab_confirm_run_pipeline(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # ID параметров для запуска
    run_id = context.user_data['run-repository-id']
    run_model: GitlabRepositoryRunsModel = get_object_or_404(GitlabRepositoryRunsModel, pk=run_id)
    repository_model = run_model.repository_model

    buttons = [
        [InlineKeyboardButton("Отменить запуск пайплайна", callback_data=str(ConversationStatesEnum.PIPELINE_RUN_NO))]
    ]

    # Запуск пайплайна.
    try:
        access_token = repository_model.gitlabrepositorytokensmodel.access_token
    except GitlabRepositoryTokensModel.DoesNotExist:
        query.message.edit_text(
            generate_pipeline_template(
                run_id,
                PipelineStatusEnum.NOT_STARTED_WITH_ERRORS,
                reason='Не найдены токены для запуска данного пайплайна!',
            )
        )
        return ConversationHandler.END

    gitlab_repo = Gitlab(url=run_model.repository_model.base_repository_model.repo_base_url, private_token=access_token)

    try:
        gitlab_repo.auth()
    except GitlabAuthenticationError:
        query.message.edit_text(
            generate_pipeline_template(
                run_id,
                PipelineStatusEnum.NOT_STARTED_WITH_ERRORS,
                reason='Некорректные токены для авторизации в Gitlab!',
            )
        )
        return ConversationHandler.END

    try:
        project = gitlab_repo.projects.get(repository_model.repository_id)
    except GitlabGetError:
        query.message.edit_text(
            generate_pipeline_template(
                run_id,
                PipelineStatusEnum.NOT_STARTED_WITH_ERRORS,
                reason=f'Некорректный ID проекта (repo-id={repository_model.repository_id})',
            )
        )
        return ConversationHandler.END

    try:
        pipeline = project.trigger_pipeline(
            ref=run_model.ref,
            token=repository_model.gitlabrepositorytokensmodel.trigger_token,
        )
        pipeline_model = GitlabRepositoryPipelineModel.objects.create(
            pipeline_id=pipeline.encoded_id,
            web_url=pipeline.attributes.get('web_url'),
            repository=repository_model,
        )
        pipeline_model_history = GitlabRepositoryPipelineHistoryModel.objects.create(
            source=pipeline.attributes,
            status=pipeline.attributes.get('status'),
            pipeline=pipeline_model,
        )
    except GitlabError as ex:
        query.message.edit_text(
            generate_pipeline_template(
                run_id,
                PipelineStatusEnum.NOT_STARTED_WITH_ERRORS,
                reason=ex.response_body.decode('utf-8'),
            )
        )
        return ConversationHandler.END

    query.edit_message_text(
        generate_pipeline_template(run_id, PipelineStatusEnum.STARTED), reply_markup=InlineKeyboardMarkup(buttons)
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
