# Generated by Django 3.2.7 on 2021-12-09 00:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20211208_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=0, related_name='peaopleliked', to=settings.AUTH_USER_MODEL),
        ),
    ]
