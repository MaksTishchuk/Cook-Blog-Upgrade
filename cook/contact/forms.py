from django import forms
from . models import ContactModel


class ContactForm(forms.ModelForm):
    """Форма обратной связи"""

    class Meta:
        model = ContactModel
        fields = '__all__'