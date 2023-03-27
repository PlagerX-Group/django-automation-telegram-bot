# Generated by Django 3.2.9 on 2023-03-27 20:19
import uuid

from django.db import migrations, models
import django.db.models.deletion


def transfer_data(apps, schema_editor):
    telegram_user_model = apps.get_model('extendeduser', 'TelegramUserModel')
    extended_user_model = apps.get_model('extendeduser', 'ExtendedUserModel')
    for old in telegram_user_model.objects.all():
        new_obj = extended_user_model()
        new_obj.user = old.user
        new_obj.telegram_user_id = old.telegram_user_id
        new_obj.gitlab_username = str(uuid.uuid4())
        new_obj.created_at = old.created_at
        new_obj.updated_at = old.updated_at
        new_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('extendeduser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedUserModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user', verbose_name='Пользователь')),
                ('telegram_user_id', models.PositiveBigIntegerField(unique=True, verbose_name='Идентификатор пользователя в Telegram')),
                ('gitlab_username', models.TextField(unique=True, verbose_name="Идентификатор Gitlab")),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Расширенные пользователи Django',
                'verbose_name_plural': 'Расширенные пользователи Django',
                'db_table': 'django_user_extended',
                'ordering': ['telegram_user_id', 'created_at', 'updated_at'],
            },
        ),
        migrations.RunPython(transfer_data),
        migrations.DeleteModel(
            name='TelegramUserModel',
        )
    ]