from django import forms
from mainapp.models import User


class ManagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "surname", "phone", 'username', 'email', 'password']


class AddManagerForm(forms.Form):
    first_name = forms.CharField(required=True,
                                max_length=255,
                                widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'First Name'
                                   }
                                ))
    surname = forms.CharField(required=True,
                                 max_length=255,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Surname'
                                     }
                                 ))
    phone = forms.CharField(required=True,
                                 max_length=255,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Phone'
                                     }
                                 ))
    username = forms.CharField(required=True,
                                 max_length=255,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Username'
                                     }
                                 ))
    email = forms.CharField(required=True,
                                 max_length=255,
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Email'
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
        cleaned_data = super().clean()

        cc_email = self.cleaned_data.get('email')
        cc_phone = self.cleaned_data.get('phone')
        cc_username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(email=cc_email)
        except User.DoesNotExist:
            user = None

        if user:
            self.add_error('email', "Already taken")
            return cleaned_data

        try:
            user_phone = User.objects.get(phone=cc_phone)
        except User.DoesNotExist:
            user_phone = None

        if user_phone:
            self.add_error('phone', "Already taken")
            return cleaned_data

        try:
            user_username = User.objects.get(username=cc_username)
        except User.DoesNotExist:
            user_username = None

        if user_username:
            self.add_error('username', "Already taken")
            return cleaned_data

        return cleaned_data
