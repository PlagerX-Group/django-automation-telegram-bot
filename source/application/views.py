import json
import logging

from application.celery import celery_app
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from telegram import Update
from telegrambot.dispatcher import dispatcher
from telegrambot.main import telegram_bot

logger = logging.getLogger(__name__)


@celery_app.task(ignore_result=True)
def process_telegram_event(update_json):
    update = Update.de_json(update_json, telegram_bot)
    dispatcher.process_update(update)


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        if settings.DEBUG:
            process_telegram_event(json.loads(request.body))
        else:
            process_telegram_event.delay(json.loads(request.body))
        return JsonResponse({'status': 'success'})

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success'})
