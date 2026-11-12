from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import AppUser

class AppUserCreationForm(UserCreationForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Provide your password'}),)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),)

    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = ('username', 'first_name', 'last_name', 'email',)
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

        help_texts = {
            'username': 'Your username must be unique',
            'first_name': 'Names must contain only letters',
            'last_name': 'Names must contain only letters',
            'email': 'Email is optional. If email is provide then it must be unique',
        }

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Please, enter your username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Please, enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Please, enter your last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Please, enter your email address'}),
        }

