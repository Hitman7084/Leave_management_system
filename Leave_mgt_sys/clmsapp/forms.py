from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    photo = forms.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'photo', 'email', 'password', 'rtpassword', 'role']