import pytest
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models.query_utils import DeferredAttribute

from extendeduser import models


class TestTelegramUserModel:
    @pytest.fixture(scope="class")
    def get_single_model(cls, django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            user = User.objects.create_user(username='username', password='password', email='example@domain.ru')
            model = models.ExtendedUserModel.objects.create(telegram_user_id=12345, user=user)
            model.full_clean()
            return model

    def test_config(self, get_single_model):
        assert get_single_model._meta.db_table == 'telegram_users'
        assert get_single_model._meta.verbose_name == 'Пользователь в Telegram'
        assert get_single_model._meta.verbose_name_plural == 'Пользователь в Telegram'

    def test_magick_str(self, get_single_model):
        assert str(get_single_model) == get_single_model.user.username

    def test_magick_repr(self, get_single_model):
        assert str(get_single_model) == get_single_model.user.username

    @pytest.mark.parametrize(
        'model_field, expected_name',
        [
            (models.ExtendedUserModel.user, 'Пользователь'),
            (models.ExtendedUserModel.telegram_user_id, 'Идентификатор пользователя в Telegram'),
            (models.ExtendedUserModel.created_at, 'Дата создания'),
            (models.ExtendedUserModel.updated_at, 'Дата обновления'),
        ],
    )
    def test_fields_verbose_name(self, model_field: DeferredAttribute, expected_name: str):
        assert model_field.field.verbose_name == expected_name

    @pytest.mark.django_db
    def test_user_one_to_one_primary_key(self):
        user = User.objects.create_user(username='username', password='password', email='example@domain.ru')
        models.ExtendedUserModel.objects.create(telegram_user_id=1, user=user)
        with pytest.raises(IntegrityError):
            models.ExtendedUserModel.objects.create(telegram_user_id=2, user=user)

    @pytest.mark.django_db
    def test_create_exists_telegram_user_id(self):
        user1 = User.objects.create_user(username='username1', password='password2', email='example1@domain.ru')
        user2 = User.objects.create_user(username='username2', password='password2', email='example2@domain.ru')
        models.ExtendedUserModel.objects.create(telegram_user_id=1, user=user1)
        with pytest.raises(IntegrityError):
            models.ExtendedUserModel.objects.create(telegram_user_id=1, user=user2)

    @pytest.mark.django_db
    def test_null_parameters(self):
        with pytest.raises(IntegrityError):
            models.ExtendedUserModel.objects.create(telegram_user_id=None)

    @pytest.mark.django_db
    def test_count_elements_in_table(self, get_single_model):
        assert models.ExtendedUserModel.objects.count() == 1

    def test_auto_now_add_field(self, get_single_model):
        assert get_single_model.created_at is not None
        assert get_single_model.updated_at is not None
        assert get_single_model.created_at.replace(microsecond=0) == get_single_model.updated_at.replace(microsecond=0)

    @pytest.mark.django_db
    def test_updated_at_auto_now_field(self, get_single_model):
        old_updated_at = get_single_model.updated_at
        old_created_at = get_single_model.created_at
        get_single_model.telegram_user_id = 10
        get_single_model.save()
        assert get_single_model.updated_at is not None
        assert get_single_model.created_at == old_created_at
        assert get_single_model.updated_at > old_updated_at
        assert get_single_model.updated_at > get_single_model.created_at

    @pytest.mark.django_db
    def test_get_user(self, tgbot_update_and_context_mock):
        update, context = tgbot_update_and_context_mock
        user = User.objects.create_user(username='username1', password='password', email='example1@domain.ru')
        models.ExtendedUserModel.objects.create(telegram_user_id=1, user=user)
        user = models.ExtendedUserModel.get_telegram_user(update, context)
        assert isinstance(user, models.ExtendedUserModel)
        assert user.telegram_user_id == 1

    @pytest.mark.django_db
    def test_get_user_not_exists(self, tgbot_update_and_context_mock):
        update, context = tgbot_update_and_context_mock
        user = models.ExtendedUserModel.get_telegram_user(update, context)
        assert user is None
