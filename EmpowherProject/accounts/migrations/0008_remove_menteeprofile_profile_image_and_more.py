# Generated by Django 5.0.3 on 2024-07-17 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_rename_profile_picture_customuser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menteeprofile',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='mentorprofile',
            name='profile_image',
        ),
    ]
