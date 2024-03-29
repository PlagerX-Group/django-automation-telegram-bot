# Generated by Django 3.2.9 on 2023-03-27 20:57

from django.db import migrations, models


def set_gitlab_username_to_nullstr(apps, schema_editor):
    extended_model = apps.get_model('extendeduser', 'ExtendedUserModel')
    for obj in extended_model.objects.all():
        obj.gitlab_username = ''
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('extendeduser', '0002_alter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendedusermodel',
            name='gitlab_username',
            field=models.TextField(verbose_name='Имя пользователя Gitlab'),
        ),
        migrations.RunPython(set_gitlab_username_to_nullstr),
    ]
