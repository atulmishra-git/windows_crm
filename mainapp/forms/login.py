from django import forms


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
