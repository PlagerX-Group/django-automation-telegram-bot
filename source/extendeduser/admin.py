from django.contrib import admin
from extendeduser.models import ExtendedUserModel


@admin.register(ExtendedUserModel)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'telegram_user_id',
        'created_at',
        'updated_at',
    ]
    search_fields = ('username', 'user_id')
