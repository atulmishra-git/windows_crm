from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

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
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                *[Row(field_name, css_class='form-group')
                  for field_name in list(self.fields.keys())[:len(self.fields.keys()) // 2 + 1]],
                css_class='col-md-6'
            ), Column(
                *[Row(field_name, css_class='form-group')
                  for field_name in list(self.fields.keys())[(len(self.fields.keys()) // 2 + 1):]],
                css_class='col-md-6'
            ),
        )

    def clean_email(self):
        if self.instance and self.instance.id:
            return self.instance.email
        return self.cleaned_data['email']
