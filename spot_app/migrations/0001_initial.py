# Generated by Django 3.1.7 on 2021-02-19 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Response_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_data', models.CharField(max_length=200, verbose_name='Исходный запрос')),
                ('request_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')),
                ('result_list', models.TextField(verbose_name='Ссылки на видео?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец запроса')),
            ],
        ),
    ]