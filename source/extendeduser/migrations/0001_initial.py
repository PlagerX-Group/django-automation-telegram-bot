from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUserModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user', verbose_name='Пользователь')),
                ('telegram_user_id', models.PositiveBigIntegerField(verbose_name='Идентификатор пользователя в Telegram')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Пользователь в Telegram',
                'verbose_name_plural': 'Пользователь в Telegram',
                'db_table': 'telegram_users',
                'ordering': ['telegram_user_id', 'created_at', 'updated_at'],
            },
        ),
    ]