from django import forms
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterUserForm(forms.Form):
    name = forms.CharField(label='name')
    surname = forms.CharField(label='surname')
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password')
    password2 = forms.CharField(label='password2')

    def clean(self):
        cd = super().clean()

        password = cd['password']
        password2 = cd['password2']
        if password != password2:
            raise ValidationError('Twoje hasła nie są identyczne!')

        email = cd['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ten login jest zajęty')


class LoginUserForm(forms.Form):
    email = forms.EmailField(label='email', required=True)
    password = forms.CharField(label='password', required=True)
