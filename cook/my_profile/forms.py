from django import forms
from .models import UserProfile


class ProfileForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=50, required=False)
    last_name = forms.CharField(label='Фамилия', max_length=50, required=False)
    phone = forms.CharField(label='Телефон', max_length=50, required=False)
    organization = forms.CharField(label='Место работы', max_length=50, required=False)
    photo = forms.ImageField(label='Фото профиля', required=False)


class SignupForm(forms.Form):

    def signup(self, request, user):
        user_profile = UserProfile()
        user_profile.user = user
        user.save()
        user_profile.save()
