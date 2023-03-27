from __future__ import annotations

import typing as t

from django.contrib.auth.models import User as _User
from django.db import models
from telegram import Update
from telegram.ext import CallbackContext
from telegrambot.utils.dto import update_to_dict


class ExtendedUserModel(models.Model):
    user = models.OneToOneField(_User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    telegram_user_id = models.PositiveBigIntegerField(unique=True, verbose_name="Идентификатор пользователя в Telegram")
    gitlab_username = models.TextField(verbose_name="Имя пользователя Gitlab")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = "django_user_extended"
        ordering = ['telegram_user_id', 'created_at', 'updated_at']
        verbose_name = "Расширенные пользователи Django"
        verbose_name_plural = "Расширенные пользователи Django"

    @classmethod
    def get_telegram_user(cls, update: Update, context: CallbackContext) -> t.Optional[ExtendedUserModel]:
        user_dict = update_to_dict(update)
        try:
            return cls.objects.get(telegram_user_id=user_dict["user_id"])
        except ExtendedUserModel.DoesNotExist:
            pass
        return None

    def __str__(self) -> str:
        return str(self.user.username)

    def __repr__(self) -> str:
        return self.__str__()
