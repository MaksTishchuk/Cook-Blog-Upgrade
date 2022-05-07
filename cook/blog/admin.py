from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin

from . import models


class RecipeInLine(admin.StackedInline):
    model = models.Recipe
    extra = 1


class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст поста', widget=CKEditorUploadingWidget())

    class Meta:
        model = models.Post
        fields = '__all__'


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    prepopulated_fields = {'slug': ('title',)}
    list_display = [
        'id', 'title', 'author', 'category', 'views', 'get_likes_count', 'get_dislikes_count',
        'create_at', 'get_image'
    ]
    list_display_links = ('id', 'title',)
    list_filter = ('category',)
    search_fields = ('title', 'text',)
    fields = (
        'title', 'slug', 'text', 'category', 'author', 'tags', 'image', 'get_image',
        'create_at', 'views', 'get_likes_count', 'likes', 'get_dislikes_count', 'dislikes',
    )
    readonly_fields = (
        'get_image', 'create_at', 'views', 'get_likes_count', 'likes', 'get_dislikes_count',
        'dislikes'
    )
    inlines = [RecipeInLine]
    save_as = True
    save_on_top = True

    def get_image(self, obj):
        """Отобразим фото в админке"""

        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100">')
        else:
            return f'Фото не установлено'

    get_image.short_description = 'Миниатюра'
    models.Post.get_likes_count.short_description = 'Лайки, шт.'
    models.Post.get_dislikes_count.short_description = 'Дизлайки, шт.'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'post', 'prep_time', 'cook_time']
    list_display_links = ('id', 'name',)
    list_filter = ('prep_time', 'cook_time')
    search_fields = ('name', )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'website', 'create_at']
    list_display_links = ('id', 'name',)


# MPTTModelAdmin позволяет сделать сдвиг вправо в админке для подкатегорий для наглядности
@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'id', 'slug', 'parent']
    list_display_links = ('id', 'name',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug']
    list_display_links = ('id', 'name',)


admin.site.site_title = 'by Maks'
admin.site.site_header = 'Управление сайтом от Макса'
