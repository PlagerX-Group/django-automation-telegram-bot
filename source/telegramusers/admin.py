from django.contrib import admin
from telegramusers.models import TelegramUserModel


@admin.register(TelegramUserModel)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'telegram_user_id',
        'created_at',
        'updated_at',
    ]
    search_fields = ('username', 'user_id')
