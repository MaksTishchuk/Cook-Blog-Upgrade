from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from my_profile.models import UserProfile
from .models import Post, Comment, Category
from .forms import CommentForm
from .filters import PostFilter
from .utils import pagination_context, sort


class HomeView(ListView):
    """View для главной страницы"""

    model = Post
    paginate_by = 9
    template_name = 'blog/home.html'

    def get_queryset(self):
        return Post.objects.all().select_related('category', 'author').prefetch_related(
            'comment', 'likes', 'dislikes'
        )


class CategoryListView(ListView):
    """View для постов по категориям, с фильтрацией"""

    model = Post

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs.get('slug')
        ).select_related('category', 'author').prefetch_related('comment', 'likes', 'dislikes')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        queryset = PostFilter(self.request.GET, queryset=self.get_queryset()).qs
        posts_number = self.request.GET.get('posts_number')
        posts_on_page = int(6 if not posts_number else posts_number)
        page_number = int(1 if not self.request.GET.get('page') else self.request.GET.get('page'))
        extra_context = pagination_context(queryset, posts_on_page, page_number)
        context['sort'] = sort(self.request.GET.items())
        context['form'] = PostFilter(self.request.GET, queryset=self.get_queryset()).form
        context['category'] = category
        context['title'] = category.name
        context.update(extra_context)
        return context


class PostDetailView(DetailView):
    """View для открытия конкретного поста"""

    model = Post
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_queryset(self):
        slug = self.kwargs.get('post_slug', '')
        q = super().get_queryset()
        post = q.filter(slug=slug).select_related('category', 'author').prefetch_related('comment')
        post.update(views=F('views') + 1)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user = self.request.user
            form = CommentForm(initial={'name': user.username, 'email': user.email})
            context['form'] = form
        else:
            context['form'] = CommentForm
        return context


def like_post(request, slug):
    """Лайк поста с помощью Ajax"""

    post = Post.objects.get(slug=slug)
    context = {}
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
            context['dislikes_count'] = post.dislikes.count()
    context['likes_count'] = post.likes.count()

    return JsonResponse(context)


def dislike_post(request, slug):
    """Дизайк поста с помощью Ajax"""

    post = Post.objects.get(slug=slug)
    context = {}

    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            context['likes_count'] = post.likes.count()

    context['dislikes_count'] = post.dislikes.count()

    return JsonResponse(context)


class CreateComment(CreateView):
    """View для создания комментария"""

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post_id = self.kwargs.get('pk')
        if self.request.user.is_authenticated:
            user_profile = get_object_or_404(UserProfile, user=self.request.user)
            if user_profile.photo:
                form.instance.profile_photo = user_profile.photo
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class UserLikedPostList(ListView):
    """Представление для вывода постов, который лайкнул пользователь"""

    model = Post
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        post = user.user_likes.all()
        return post.select_related('category', 'author').prefetch_related(
            'comment', 'likes', 'dislikes'
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liked Posts'
        context['my_filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class SearchPostList(ListView):
    """Представление для поиска постов"""

    model = Post
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            title__icontains=self.request.GET.get('query')
        ).select_related('category', 'author').prefetch_related('comment', 'likes', 'dislikes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = f'query={self.request.GET.get("query")}&'
        context['title'] = 'Search'
        return context


class TagPostList(ListView):
    """Представление для поиска постов по тегу"""

    model = Post
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            tags=self.kwargs.get('id')
        ).select_related('category', 'author').prefetch_related('comment', 'likes', 'dislikes')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Tag'
        return context
