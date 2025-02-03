from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-register'}))
    photo = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-register'}))

    class Meta:
        model = User
        fields = ['username', 'full_name', 'photo', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-register'}),
            'full_name': forms.TextInput(attrs={'class': 'form-register'}),
            'role': forms.Select(attrs={'class': 'form-register'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-register'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-register'}),
        }

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-register'}))