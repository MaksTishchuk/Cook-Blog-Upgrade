from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """Модель категорий блюд с MPTT библиотекой для моделей, где нужно строить завязки категорий
    на категориях (не нужно самому строить деревья категорий)"""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    name = models.CharField(max_length=100, verbose_name='Наименование категории')
    slug = models.SlugField(max_length=100, verbose_name='URL категории')
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']


class Tag(models.Model):
    """Модель тегов"""

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    name = models.CharField(max_length=100, verbose_name='Тег')
    slug = models.SlugField(max_length=100, verbose_name='URL тега')

    def __str__(self):
        return self.name


class Post(models.Model):
    """Модель постов"""

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-create_at']

    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField(max_length=200, verbose_name='Наименование поста')
    image = models.ImageField(upload_to='articles/', verbose_name='Изображение поста')
    text = models.TextField(verbose_name='Текст поста')
    category = models.ForeignKey(
        Category,
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name='post', verbose_name='Теги')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    slug = models.SlugField(max_length=200, default='', unique=True, verbose_name='URL поста')
    views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')
    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
        default=None,
        blank=True,
        verbose_name='Лайки'
    )
    dislikes = models.ManyToManyField(
        User,
        related_name='user_dislikes',
        default=None,
        blank=True,
        verbose_name='Дизлайки'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_single', kwargs={'slug': self.category.slug, 'post_slug': self.slug})

    def get_recipes(self):
        return self.recipe.all()

    def get_comments(self):
        return self.comment.all()

    def get_likes_count(self):
        return self.likes.count()

    def get_dislikes_count(self):
        return self.dislikes.count()


class Recipe(models.Model):
    """Модель рецепта блюда"""

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-id']

    name = models.CharField(max_length=100, verbose_name='Наименование рецепта')
    serves = models.CharField(max_length=50, verbose_name='На сколько человек')
    prep_time = models.PositiveIntegerField(default=0, verbose_name='Время подготовки (минут)')
    cook_time = models.PositiveIntegerField(default=0, verbose_name='Время приготовления (минут)')
    ingredients = RichTextField(verbose_name='Ингридиенты')
    directions = RichTextField(verbose_name='Шаги для приготовления')
    post = models.ForeignKey(
        Post,
        related_name='recipe',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Для поста'
    )


class Comment(models.Model):
    """Модель комментариев"""

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-create_at']

    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    email = models.EmailField(max_length=100, verbose_name='Email-адрес')
    website = models.CharField(max_length=150, blank=True, null=True, verbose_name='Сайт')
    message = models.TextField(max_length=500, verbose_name='Текст сообщения')
    create_at = models.DateTimeField(default=timezone.now, verbose_name='Дата комментария')
    post = models.ForeignKey(
        Post,
        related_name='comment',
        on_delete=models.CASCADE,
        verbose_name='К посту'
    )
    profile_photo = models.ImageField(
        upload_to='comment/photos/%Y/%m/%d/',
        blank=True,
        verbose_name='Фото профиля'
    )
