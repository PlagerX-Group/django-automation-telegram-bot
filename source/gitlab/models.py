from django.db import models


class GitlabRepositoryModel(models.Model):
    repo_link = models.URLField(max_length=255, null=False, unique=True, verbose_name="Ссылка на репозиторий в Gitlab")
    target_ref = models.TextField(
        max_length=64,
        null=False,
        default="master",
        verbose_name="Ветка для запуска пайплайна",
    )
    repo_name = models.TextField(max_length=128, null=False, verbose_name="Наименование проекта")
    description = models.TextField(max_length=64, null=True, verbose_name="Описание репозитория")
    is_active = models.BooleanField(default=True, verbose_name="Активен ли репозиторий")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_repository"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. Репозитории"
        verbose_name_plural = "Gitlab. Репозитории"

    def __str__(self) -> str:
        return str(self.repo_link)


class GitlabRepositoryTokensModel(models.Model):
    gitlab_repository = models.OneToOneField(
        GitlabRepositoryModel,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Gitlab Репозиторий",
    )
    trigger_token = models.TextField(max_length=64, null=False, verbose_name="Токен для доступа к Gitlab")
    private_token = models.TextField(max_length=64, null=False, verbose_name="Приватный токен доступа к Gitlab")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_repository_trigger_token"
        verbose_name = "Gitlab. Токены"
        verbose_name_plural = "Gitlab. Токены"

    def __str__(self) -> str:
        return str(self.gitlab_repository)


class GitlabRepositoryPipelineModel(models.Model):
    pipeline_id = models.BigIntegerField(unique=True, verbose_name="ID пайплайна")
    web_url = models.URLField(verbose_name="URL пайплайна")
    source = models.JSONField(default=dict, verbose_name="Исходный ответ JSON от Gitlab")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Дата обновления")
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
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "gitlab_repository_pipeline_history"
        ordering = ['created_at', 'updated_at']
        verbose_name = "Gitlab. История Pipelines"
        verbose_name_plural = "Gitlab. История Pipelines"

    def __str__(self) -> str:
        return f"Pipeline #{self.pipeline.pipeline_id}"
