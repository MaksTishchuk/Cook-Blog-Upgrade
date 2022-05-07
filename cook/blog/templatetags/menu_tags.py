import requests
from django import template
from ..models import Category, Post

register = template.Library()


def get_all_categories():
    return Category.objects.all().prefetch_related('post')


@register.simple_tag()
def get_list_category():
    """Вывод всех категорий"""

    return get_all_categories()


@register.inclusion_tag('blog/include/tags/top_menu.html')
def get_categories():
    """Вывод списка категорий"""

    category = get_all_categories()
    return {'list_category': category}


@register.inclusion_tag('blog/include/tags/recipes_tag.html')
def get_last_posts():
    """Вывод последних 5 постов в меню"""

    posts = Post.objects.select_related('category').order_by('-id')[:5]
    return {'list_last_post': posts}


@register.inclusion_tag('blog/include/tags/exchange_rates.html')
def get_exchange_rate():
    """Вывод курса валют"""

    exchange_rates = requests.get(
        'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    )
    if exchange_rates.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = exchange_rates.json()
    return {'exchange_rates': data}
