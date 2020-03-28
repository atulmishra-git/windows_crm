from django import forms
from django.core.exceptions import ValidationError

from mainapp.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               max_length=255,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Username'
                                   }
                               ))

    password = forms.CharField(required=True,
                               max_length=255,
                               widget=forms.PasswordInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Password'
                                   }
                               ))

    def clean(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username__iexact=username).exists():
            raise ValidationError(
                "Username/Password does not match"
            )
        user = User.objects.get(username__iexact=username)
        password = self.cleaned_data['password']
        if not user.check_password(raw_password=password):
            raise ValidationError(
                "Username/Password does not match"
            )
        return self.cleaned_data
