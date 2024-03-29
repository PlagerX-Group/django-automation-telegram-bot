# Generated by Django 3.2.9 on 2023-03-25 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gitlabapp', '0008_auto_20230325_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlabrepositorybasemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorybasemodel',
            name='repo_base_url',
            field=models.URLField(unique=True, verbose_name='Базовая ссылка на URL'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorybasemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorymodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorymodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorypipelinehistorymodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorypipelinehistorymodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorypipelinemodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorypipelinemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositoryrunsmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositoryrunsmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorytokensmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='gitlabrepositorytokensmodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
    ]
