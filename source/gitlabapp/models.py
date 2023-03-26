from django.db import models


class GitlabRepositoryBaseModel(models.Model):
    repo_base_url = models.URLField(null=False, unique=True, verbose_name="Базовая ссылка на URL")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_services"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. Сервисы"
        verbose_name_plural = "Gitlab. Сервисы"

    def __str__(self) -> str:
        return self.repo_base_url

    def __repr__(self) -> str:
        return self.__str__()


class GitlabRepositoryModel(models.Model):
    repository_id = models.BigIntegerField(blank=True, unique=True, verbose_name="ID репозитория в Gitlab")
    name = models.TextField(max_length=128, null=False, verbose_name="Наименование проекта")
    description = models.TextField(max_length=64, null=True, verbose_name="Описание репозитория")
    is_active = models.BooleanField(default=True, verbose_name="Активен ли репозиторий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    base_repository_model = models.ForeignKey(GitlabRepositoryBaseModel, on_delete=models.CASCADE, verbose_name="Базовый репозиторий")

    class Meta:
        db_table = "gitlab_repository"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. Репозитории"
        verbose_name_plural = "Gitlab. Репозитории"

    def __str__(self) -> str:
        return str(self.name)


class GitlabRepositoryRunsModel(models.Model):
    name = models.TextField(max_length=128, null=False, verbose_name="Наименование параметров")
    ref = models.TextField(
        max_length=64,
        null=False,
        default="master",
        verbose_name="Ветка для запуска пайплайна",
    )
    description = models.TextField(max_length=64, null=True, verbose_name="Описание параметров")
    variables = models.JSONField(verbose_name="JSON с параметрами для создания пайплайна")
    is_active = models.BooleanField(default=True, verbose_name="Активны ли параметры")
    warning_message = models.TextField(default='', max_length=255, verbose_name="Сообщение-предупреждение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    repository_model = models.ForeignKey(GitlabRepositoryModel, on_delete=models.CASCADE, verbose_name="Модель репозитория")

    class Meta:
        db_table = "gitlab_runs"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. Запуск"
        verbose_name_plural = "Gitlab. Запуск"

    def __str__(self) -> str:
        return str(self.name)


class GitlabRepositoryTokensModel(models.Model):
    gitlab_repository = models.OneToOneField(
        GitlabRepositoryModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Gitlab Репозиторий",
    )
    trigger_token = models.TextField(max_length=64, null=False, verbose_name="Триггер-токен для доступа к Gitlab")
    access_token = models.TextField(max_length=64, null=False, verbose_name="Токен доступа к Gitlab проекту")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_repository_trigger_token"
        verbose_name = "Gitlab. Токены"
        verbose_name_plural = "Gitlab. Токены"

    def __str__(self) -> str:
        return str(self.gitlab_repository)


class GitlabRepositoryPipelineModel(models.Model):
    pipeline_id = models.BigIntegerField(unique=True, verbose_name="ID пайплайна")
    web_url = models.URLField(verbose_name="URL пайплайна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    repository = models.ForeignKey(GitlabRepositoryModel, on_delete=models.CASCADE, verbose_name="Репозиторий")

    class Meta:
        db_table = "gitlab_repository_pipeline"
        ordering = ['id', 'created_at', 'updated_at']
        verbose_name = "Gitlab. Pipeline"
        verbose_name_plural = "Gitlab. Pipeline"

    def __str__(self) -> str:
        return f"Pipeline #{self.pipeline_id}"


class GitlabRepositoryPipelineHistoryModel(models.Model):
    pipeline = models.OneToOneField(
        GitlabRepositoryPipelineModel,
        on_delete=models.CASCADE,
        verbose_name="Gitlab. Pipeline",
    )
    source = models.JSONField(default=dict, verbose_name="Исходный ответ JSON от Gitlab")
    status = models.TextField(null=False, verbose_name="Статус пайплайна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_repository_pipeline_history"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. История Pipelines"
        verbose_name_plural = "Gitlab. История Pipelines"

    def __str__(self) -> str:
        return f"Pipeline #{self.pipeline.pipeline_id}"
