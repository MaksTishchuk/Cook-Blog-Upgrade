from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ContactModel, ContactLink, About, Social, ImageAbout


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    """Регистрируем модель обратной связи в административной панели"""

    list_display = ['id', 'name', 'email', 'website', 'create_at']
    list_display_links = ('id', 'name',)


class ImageAboutInLIne(admin.StackedInline):
    model = ImageAbout
    extra = 1


@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    """Регистрируем модель страницы о нас"""

    list_display = ['id', 'name', ]
    list_display_links = ('id', 'name',)
    inlines = (ImageAboutInLIne, )


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    """Регистрируем модель страницы о нас"""

    list_display = ['id', 'name', 'link', 'get_icon']
    list_display_links = ('id', 'name',)
    fields = (
        'name', 'link', 'icon', 'get_icon',
    )
    readonly_fields = ('get_icon',)

    def get_icon(self, obj):
        """Отобразим фото в админке"""

        if obj.icon:
            return mark_safe(f'<img src="{obj.icon.url}" width="50">')
        else:
            return f'Фото не установлено'

    get_icon.short_description = 'Иконка'


admin.site.register(ContactLink)
