from django.db import models


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    profile_photo = models.ImageField(
        upload_to='chat/photos/%Y/%m/%d/',
        blank=True,
    )

    class Meta:
        ordering = ('date_added',)
