from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views import View
from telegram import Update
from telegrambot.dispatcher import dispatcher


class TelegramBotWebhookView(View):
    def post(self, request: WSGIRequest, *args, **kwargs):
        # update = Update.de_json(request.body.decode('utf-8'))
        # dispatcher.process_update(update)
        pass

    def get(self, request, *args, **kwargs):
        return JsonResponse({'status': 'success'})
