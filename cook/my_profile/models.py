from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Телефон')
    organization = models.CharField(max_length=128, blank=True, verbose_name='Место работы')
    photo = models.ImageField(
        upload_to='profile_photos/%Y/%m/%d/',
        blank=True,
        verbose_name='Фото профиля'
    )
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return self.user.__str__()

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False
