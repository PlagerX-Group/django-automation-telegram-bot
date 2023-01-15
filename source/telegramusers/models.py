from __future__ import annotations

import typing as t

from django.contrib.auth.models import User as _User
from django.db import models
from telegram import Update
from telegram.ext import CallbackContext

from telegrambot.handlers.utils.dto import update_to_dict


class TelegramUserModel(models.Model):
    user = models.OneToOneField(_User, on_delete=models.CASCADE, primary_key=True)
    telegram_user_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        db_table = "telegram_users"
        ordering = ['telegram_user_id', 'created_at', 'updated_at']

    @classmethod
    def get_user(cls, update: Update, context: CallbackContext) -> t.Optional[TelegramUserModel]:
        user_dict = update_to_dict(update)
        try:
            user = cls.objects.get(telegram_user_id=user_dict["user_id"])

            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(user_dict["user_id"]).strip():
                    user.deep_link = payload
                    user.save()
            return user
        except TelegramUserModel.DoesNotExist:
            pass
        return None

    def __str__(self) -> str:
        return str(self.user.username)

    def __repr__(self) -> str:
        return self.__str__()
