from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from allauth.account.views import PasswordChangeView


class MyPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('my_profile')


@login_required
def profile(request):
    """ Страница профиля """
    user = request.user
    return render(request, 'account/my_profile.html', {'user': user})


@login_required
def profile_update(request):
    """ Страница изменения профиля """
    user = request.user
    if UserProfile.objects.filter(user=user):
        user_profile = UserProfile.objects.get(user=user)
    else:
        user_profile = UserProfile.objects.create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            user_profile.phone = form.cleaned_data['phone']
            user_profile.organization = form.cleaned_data['organization']
            if form.cleaned_data['photo']:
                user_profile.photo = form.cleaned_data['photo']
            user_profile.save()

            return HttpResponseRedirect(reverse('my_profile'))
    else:
        default_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone': user_profile.phone,
            'organization': user_profile.organization,
            'photo': user_profile.photo,
        }
        form = ProfileForm(default_data)

    return render(request, 'account/my_profile_update.html', {'form': form, 'user': user})
