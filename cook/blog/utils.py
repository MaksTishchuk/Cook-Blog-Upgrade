from django.core.paginator import Paginator
import requests


def pagination_context(queryset, number_of_posts=6, page_number=1):
    paginator = Paginator(queryset, number_of_posts)
    page_obj = paginator.get_page(page_number)
    post_list = paginator.page(page_number)
    extra_context = {
        'post_list': post_list,
        'paginator': paginator,
        'page_obj': page_obj
    }
    return extra_context


def sort(get_params):
    sort_params = ''
    for k, v in get_params:
        if v and (k != 'page' or k != 'posts_number'):
            sort_params += f'{k}={v}&'
    return sort_params
