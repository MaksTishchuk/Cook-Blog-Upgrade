from ckeditor.fields import RichTextField
from django.db import models


class ContactModel(models.Model):
    """Модель обратной связи"""

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-create_at']

    name = models.CharField(max_length=50, verbose_name='Name')
    email = models.EmailField(verbose_name='Email')
    website = models.URLField(blank=True, null=True, verbose_name='Site')
    message = models.TextField(max_length=5000, verbose_name='Message')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Create_at')

    def __str__(self):
        return f'{self.name} - {self.email}'


class ContactLink(models.Model):
    """Модель контактов"""

    class Meta:
        verbose_name = 'Контактные данные'
        verbose_name_plural = 'Контактные данные'
        ordering = ['-id']

    icon = models.FileField(upload_to='icons/', verbose_name='Иконка')
    name = models.CharField(
        max_length=200,
        verbose_name='Информация для пользователей (номер, почта и тд.)'
    )

    def __str__(self):
        return f'{self.name}'


class About(models.Model):
    """Модель страницы о нас"""

    class Meta:
        verbose_name = 'Страница "О нас"'
        verbose_name_plural = 'Страница "О нас"'
        ordering = ['-id']

    name = models.CharField(max_length=50, default='', verbose_name='Наименование')
    text = RichTextField(verbose_name='Текст страницы "О нас"')
    mini_text = RichTextField(verbose_name='Коротенький текст для предпросмотра')

    def get_first_image(self):
        item = self.about_images.first()
        return item.image.url

    def get_images(self):
        return self.about_images.order_by('id')[1:]


class ImageAbout(models.Model):
    """Модель изображений для страницы о нас"""

    class Meta:
        verbose_name = 'Изображения для страницы "О нас"'
        verbose_name_plural = 'Изображения для страницы "О нас"'
        ordering = ['-id']

    image = models.ImageField(upload_to='about/', verbose_name='Изображение')
    page = models.ForeignKey(
        About,
        on_delete=models.CASCADE,
        related_name='about_images',
        verbose_name='Для страницы "О нас"'
    )
    alt = models.CharField(max_length=100, verbose_name='Текст, если картинка не загрузится')


class Social(models.Model):
    """Модель социальных ссылок"""

    class Meta:
        verbose_name = 'Социальные ссылки'
        verbose_name_plural = 'Социальные ссылки'
        ordering = ['-id']

    icon = models.FileField(upload_to='icons/', verbose_name='Иконка')
    name = models.CharField(max_length=200, verbose_name='Наименование социальной ссылки')
    link = models.URLField(verbose_name='Ссылка')

    def __str__(self):
        return f'{self.name}'
