# Generated by Django 5.0.3 on 2024-07-18 12:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_customuser_date_joined'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='linkedin',
        ),
        migrations.AddField(
            model_name='menteeprofile',
            name='linkedin',
            field=models.URLField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mentorprofile',
            name='linkedin',
            field=models.URLField(default=88),
            preserve_default=False,
        ),
    ]
