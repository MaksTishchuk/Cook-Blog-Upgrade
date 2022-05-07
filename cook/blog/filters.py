import django_filters

from .models import *


class PostFilter(django_filters.FilterSet):
    """Django-filter для постов"""

    CHOICES_SORT = (
        ("-create_at", 'Сначала новые'),
        ("create_at", 'Сначала старые'),
        ("title", 'По алфавиту'),
        ("-title", 'Обратный порядок'),
        ("-views", 'По просмотрам')
    )
    CHOICES_POSTS_NUMBER = (
        (6, '6'),
        (8, '8'),
        (10, '10'),
        (12, '12'),
        (20, '20')
    )

    views__gt = django_filters.NumberFilter(field_name='views', lookup_expr='gt')

    ordering = django_filters.ChoiceFilter(
        label='Сортировка',
        choices=CHOICES_SORT,
        method='filter_by_order'
    )

    posts_number = django_filters.ChoiceFilter(
        label='Постов на странице',
        choices=CHOICES_POSTS_NUMBER,
        method='filter_posts_number'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains', ],
            'text': ['icontains', ],

        }

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)

    def filter_posts_number(self, queryset, name, value):
        return queryset
