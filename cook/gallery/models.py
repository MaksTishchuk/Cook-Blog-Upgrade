from django.db import models


class Photo(models.Model):
    """Модель фото для галереи"""

    class Meta:
        verbose_name = 'Фото для галереи'
        verbose_name_plural = 'Фото для галереи'
        ordering = ['-create_date']

    name = models.CharField(max_length=250, verbose_name='Наименование фото')
    image = models.ImageField(upload_to='gallery', verbose_name='Фото')
    captions = models.TextField(blank=True, verbose_name='Подпись')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    slug = models.SlugField(max_length=255, verbose_name='URL фото')

    def __str__(self):
        return self.name


class Gallery(models.Model):
    """Модель галереи"""

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галереи'
        ordering = ['-create_date']

    name = models.CharField(max_length=250, verbose_name='Наименование галереи')
    images = models.ManyToManyField(Photo, related_name='photo', verbose_name='Фото галереи')
    captions = models.TextField(max_length=250, blank=True, verbose_name='Подпись к галерее')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=255, verbose_name='URL галереи')

    def __str__(self):
        return self.name
