import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('telegram-bot-webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
]

if settings.DEBUG:
    urlpatterns.extend(
        [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    )
