import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from telegrambot import views as tgviews

admin.site.site_header = "Администрирование Telegram Bot"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('telegram-bot-webhook/', csrf_exempt(tgviews.TelegramBotWebhookView.as_view())),
]


if settings.DEBUG:
    urlpatterns.extend(
        [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    )
