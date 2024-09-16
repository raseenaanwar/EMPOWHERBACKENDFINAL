# Generated by Django 5.0.8 on 2024-08-19 05:18

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('mentee', models.ForeignKey(limit_choices_to={'user_type': 'mentee'}, on_delete=django.db.models.deletion.CASCADE, related_name='mentee_chats', to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(limit_choices_to={'user_type': 'mentor'}, on_delete=django.db.models.deletion.CASCADE, related_name='mentor_chats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.TextField(blank=True)),
                ('message_type', models.CharField(choices=[('text', 'Text'), ('file', 'File')], default='text', max_length=10)),
                ('attachment_url', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chatapp.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_url', models.URLField()),
                ('file_type', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='attachment', to='chatapp.message')),
            ],
        ),
    ]
