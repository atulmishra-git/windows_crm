from django import forms

from mainapp.forms.mixins import LabelAdder
from mainapp.models import User


class ManagerForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "surname", "phone", 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id is not None:
            self.fields['email'].widget.attrs['readonly'] = True
            self.initial['password'] = ""

    def clean_email(self):
        if self.instance and self.instance.id:
            return self.instance.email
        return self.cleaned_data['email']
