# Generated by Django 3.2.9 on 2023-03-24 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gitlabapp', '0003_gitlabrepositoryruns_ref'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GitlabRepositoryRuns',
            new_name='GitlabRepositoryRunsModel',
        ),
    ]