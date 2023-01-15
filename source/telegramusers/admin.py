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

    # actions = ['broadcast']
    #
    # def broadcast(self, request, queryset):
    #     """Select telegramusers via check mark in django-admin panel, then select "Broadcast" to send message"""
    #     user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
    #     if 'apply' in request.POST:
    #         broadcast_message_text = request.POST["broadcast_text"]
    #
    #         if DEBUG:  # for test / debug purposes - run in same thread
    #             for user_id in user_ids:
    #                 send_one_message(
    #                     user_id=user_id,
    #                     text=broadcast_message_text,
    #                 )
    #             self.message_user(request, f"Just broadcasted to {len(queryset)} telegramusers")
    #         else:
    #             broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
    #             self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")
    #
    #         return HttpResponseRedirect(request.get_full_path())
    #     else:
    #         form = BroadcastForm(initial={'_selected_action': user_ids})
    #         return render(
    #             request, "admin/templates/admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
    #         )
