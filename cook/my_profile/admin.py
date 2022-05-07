from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'phone', 'organization', 'get_photo']
    list_display_links = ('id', 'user',)
    search_fields = ('user', 'organization',)
    fields = ('user', 'phone', 'organization', 'photo', 'get_photo')
    readonly_fields = ('get_photo',)
    save_as = True
    save_on_top = True

    def get_photo(self, obj):
        """Отобразим фото в админке"""

        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="80">')
        else:
            return f'Фото не установлено'

    get_photo.short_description = 'Фото профиля'
