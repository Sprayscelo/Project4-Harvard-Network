# Generated by Django 3.2.7 on 2021-11-10 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_user_followers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='followers',
            new_name='following',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
