import uuid

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.query_utils import DeferredAttribute

from gitlabapp import models


class TestGitlabRepositoryBaseModel:
    @pytest.fixture(scope="class")
    def get_single_model(cls, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            model = models.GitlabRepositoryBaseModel.objects.create(repo_base_url='https://repo-base-url.ru')
            model.full_clean()
            return model

    def test_config(self, get_single_model):
        assert get_single_model._meta.db_table == 'gitlab_services'
        assert get_single_model._meta.verbose_name == 'Gitlab. Сервисы'
        assert get_single_model._meta.verbose_name_plural == 'Gitlab. Сервисы'

    def test_magick_str(self, get_single_model):
        assert str(get_single_model) == get_single_model.repo_base_url

    def test_magick_repr(self, get_single_model):
        assert str(get_single_model) == get_single_model.repo_base_url

    @pytest.mark.parametrize(
        'model_field, expected_name',
        [
            (models.GitlabRepositoryBaseModel.repo_base_url, 'Базовая ссылка на URL'),
            (models.GitlabRepositoryBaseModel.created_at, 'Дата создания'),
            (models.GitlabRepositoryBaseModel.updated_at, 'Дата обновления'),
        ],
    )
    def test_fields_verbose_name(self, model_field: DeferredAttribute, expected_name: str):
        assert model_field.field.verbose_name == expected_name

    @pytest.mark.django_db
    def test_null_parameters(self):
        with pytest.raises(IntegrityError):
            models.GitlabRepositoryBaseModel.objects.create(repo_base_url=None)

    @pytest.mark.django_db
    def test_create_two_unique_parameters(self):
        unique_repo_base_url = f'https://{uuid.uuid4()}.ru'
        models.GitlabRepositoryBaseModel.objects.create(repo_base_url=unique_repo_base_url)
        with pytest.raises(IntegrityError):
            models.GitlabRepositoryBaseModel.objects.create(repo_base_url=unique_repo_base_url)

    @pytest.mark.django_db
    def test_maximum_length_correct(self):
        model = models.GitlabRepositoryBaseModel.objects.create(repo_base_url=f'http://example.ru/{"a" * 182}')
        model.full_clean()

    @pytest.mark.django_db
    def test_maximum_length_error(self):
        model = models.GitlabRepositoryBaseModel.objects.create(repo_base_url=f'http://example.ru/{"a" * 183}')
        with pytest.raises(ValidationError):
            model.full_clean()

    @pytest.mark.django_db
    def test_count_elements_in_table(self, get_single_model):
        assert models.GitlabRepositoryBaseModel.objects.count() == 1

    def test_invalid_url(self, get_single_model):
        get_single_model.repo_base_url = 'invalid url'
        with pytest.raises(ValidationError):
            get_single_model.full_clean()

    def test_auto_now_add_field(self, get_single_model):
        assert get_single_model.created_at is not None
        assert get_single_model.updated_at is not None
        assert get_single_model.created_at.replace(microsecond=0) == get_single_model.updated_at.replace(microsecond=0)

    @pytest.mark.django_db
    def test_updated_at_auto_now_field(self, get_single_model):
        old_updated_at = get_single_model.updated_at
        old_created_at = get_single_model.created_at
        get_single_model.repo_base_url = 'https://example.ru/'
        get_single_model.save()
        assert get_single_model.updated_at is not None
        assert get_single_model.created_at == old_created_at
        assert get_single_model.updated_at > old_updated_at
        assert get_single_model.updated_at > get_single_model.created_at


class TestGitlabRepositoryModel:
    pass
