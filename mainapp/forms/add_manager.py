from django import forms
from mainapp.models import User


class ManagerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "surname", "phone", 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, val in self.fields.items():
            self.fields[key].widget.attrs['placeholder'] = self.fields[key].label
        if self.instance and self.instance.id is not None:
            self.fields['email'].widget.attrs['readonly'] = True
            self.initial['password'] = ""

    def clean_email(self):
        if self.instance and self.instance.id:
            return self.instance.email
        return self.cleaned_data['email']
