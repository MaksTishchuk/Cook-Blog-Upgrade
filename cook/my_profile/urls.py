from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import profile, profile_update, MyPasswordChangeView

urlpatterns = [
    path('profile/', profile, name='my_profile'),
    path('profile/update/', profile_update, name='my_profile_update'),
    path(
        'password/change/',
        login_required(MyPasswordChangeView.as_view()),
        name='account_change_password_my'
    ),
]
# http://127.0.0.1:8000/accounts/github/complete/
