from .models import Ad, Response
from allauth.account.forms import SignupForm
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CKEditor5FieldForm(forms.Form):
    content = forms.CharField(widget=CKEditor5Widget(attrs={'class': 'form-control'}))

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditor5Widget(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
            'category': 'Категория',
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': 'Текст отклика',
        }

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)