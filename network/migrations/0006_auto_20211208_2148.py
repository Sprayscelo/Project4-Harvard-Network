# Generated by Django 3.2.7 on 2021-12-09 00:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_user_following'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['timestamp']},
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(default=0, related_name='peaopleliked', to=settings.AUTH_USER_MODEL),
        ),
    ]
