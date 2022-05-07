from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма комментариев к посту"""

    class Meta:
        model = Comment
        exclude = ['create_at', 'post', 'profile_photo']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'})
        }


class CommentFormAuth(forms.ModelForm):
    """Форма комментариев к посту"""

    class Meta:
        model = Comment
        exclude = ['create_at', 'post', 'profile_photo', 'name', 'email']
        widgets = {
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message'})
        }


class SortForm(forms.Form):
    sort_posts = forms.TypedChoiceField(
        label='Сортировать',
        choices=[
            ('1', 'Сначала новые'),
            ('2', 'Сначала старые'),
            ('3', 'По алфавиту'),
            ('4', 'Обратный порядок'),
            ('5', 'По просмотрам')
        ]
    )
    quantity_posts = forms.TypedChoiceField(
        label='Постов на странице',
        choices=[
            ('6', '6'),
            ('8', '8'),
            ('10', '10'),
            ('12', '12'),
            ('20', '20')
        ]
    )
