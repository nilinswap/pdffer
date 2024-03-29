# Generated by Django 3.2 on 2022-08-05 17:39

import datetime
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('last_logged_in', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('api_key', models.CharField(max_length=500, unique=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'invite',
            },
        ),
        migrations.CreateModel(
            name='VerificationEmailLinkEntry',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cauth.client')),
            ],
            options={
                'db_table': 'verification_email_link_entry',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cauth.client')),
            ],
            options={
                'db_table': 'session',
            },
        ),
        migrations.AddField(
            model_name='client',
            name='invite',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cauth.invite'),
        ),
    ]
