# Generated by Django 5.0.7 on 2024-07-20 14:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('request', models.TextField()),
                ('assistant_content', models.TextField(blank=True, null=True)),
                ('response', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Messages',
                'managed': True,
            },
        ),
    ]
