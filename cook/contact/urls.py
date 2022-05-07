from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('contact/', cache_page(60 * 15)(views.ContactView.as_view()), name='contact'),
    path('about/', cache_page(60 * 15)(views.AboutView.as_view()), name='about'),
    path('feedback/', views.CreateFeedback.as_view(), name='feedback'),
]