# Generated by Django 3.2 on 2022-07-08 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appmigrations', '0002_auto_20220708_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='session_id',
        ),
    ]