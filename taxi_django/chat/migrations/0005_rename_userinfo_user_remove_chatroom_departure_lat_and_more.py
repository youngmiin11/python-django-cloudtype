# Generated by Django 4.2.13 on 2024-06-10 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_userinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInfo',
            new_name='User',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='departure_lat',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='departure_lng',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='destination_lat',
        ),
        migrations.RemoveField(
            model_name='chatroom',
            name='destination_lng',
        ),
    ]