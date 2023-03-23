from django.contrib import admin
from gitlab import models


@admin.register(models.GitlabRepositoryModel)
class GitlabRepositoryAdmin(admin.ModelAdmin):
    list_display = [
        'repo_link',
        'description',
        'is_active',
        'created_at',
        'updated_at',
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
