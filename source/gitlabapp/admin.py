from django.contrib import admin
from gitlabapp import models


@admin.register(models.GitlabRepositoryBaseModel)
class GitlabRepositoryAdmin(admin.ModelAdmin):
    list_display = [
        'repo_base_url',
        'created_at',
        'updated_at',
    ]


@admin.register(models.GitlabRepositoryModel)
class GitlabRepositoryAdmin(admin.ModelAdmin):
    list_display = [
        'repository_id',
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
        'base_repository_model',
    ]


@admin.register(models.GitlabRepositoryRunsModel)
class GitlabRunsAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'is_active',
        'created_at',
        'updated_at',
        'repository_model',
    ]


@admin.register(models.GitlabRepositoryPipelineModel)
class GitlabRepositoryPipelineAdmin(admin.ModelAdmin):
    list_display = [
        'pipeline_id',
        'repository',
        'created_at',
        'updated_at',
    ]


@admin.register(models.GitlabRepositoryPipelineHistoryModel)
class GitlabRepositoryPipelineHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'pipeline',
        'created_at',
        'updated_at',
    ]


@admin.register(models.GitlabRepositoryTokensModel)
class GitlabRepositoryTriggerTokenAdmin(admin.ModelAdmin):
    list_display = [
        'gitlab_repository',
        'created_at',
        'updated_at',
    ]
