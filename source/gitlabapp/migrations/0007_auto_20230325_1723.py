# Generated by Django 3.2.9 on 2023-03-25 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitlabapp', '0006_rename_parameters_gitlabrepositoryrunsmodel_variables'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gitlabrepositorytokensmodel',
            name='private_token',
        ),
        migrations.AddField(
            model_name='gitlabrepositorytokensmodel',
            name='access_token',
            field=models.TextField(default='', max_length=64, verbose_name='Токен доступа к Gitlab проекту'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gitlabrepositorytokensmodel',
            name='trigger_token',
            field=models.TextField(max_length=64, verbose_name='Триггер-токен для доступа к Gitlab'),
        ),
    ]
