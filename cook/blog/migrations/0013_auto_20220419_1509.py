# Generated by Django 3.2.6 on 2022-04-19 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20220419_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='likes',
        ),
    ]
