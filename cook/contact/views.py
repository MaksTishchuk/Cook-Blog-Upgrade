from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from .forms import ContactForm
from .models import ContactLink, About


class ContactView(View):
    """Представление страницы с контактами"""

    def get(self, request):
        contacts = ContactLink.objects.all()
        form = ContactForm
        return render(request, 'contact/contact.html', context={'contacts': contacts, 'form': form})


class CreateFeedback(CreateView):
    """Представление формы обратной связи"""

    form_class = ContactForm
    success_url = '/'


class AboutView(View):
    """Представление страницы о нас"""

    def get(self, request):
        about = About.objects.last()
        return render(request, 'contact/about.html', context={'about': about})
