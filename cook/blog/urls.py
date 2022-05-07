from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('like/<str:slug>/', views.like_post, name='like_post'),
    path('dislike/<str:slug>/', views.dislike_post, name='dislike_post'),
    path('liked-posts/', views.UserLikedPostList.as_view(), name='user_liked_posts'),
    path('comment/<int:pk>/', views.CreateComment.as_view(), name='create_comment'),
    path('search/', views.SearchPostList.as_view(), name='search'),
    path('tag/<int:id>/', views.TagPostList.as_view(), name='tag'),
    path('<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post_single'),
    path('<slug:slug>/', views.CategoryListView.as_view(), name='post_list'),
]
