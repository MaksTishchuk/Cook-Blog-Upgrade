# Generated by Django 3.2.6 on 2022-05-06 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to='chat/photos/%Y/%m/%d/'),
        ),
    ]
