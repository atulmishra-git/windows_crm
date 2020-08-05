from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column

from mainapp.forms.mixins import LabelAdder
from mainapp.models import Reseller


class ResellerForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = Reseller
        fields = ["name", "surname", "company_name", "phone", "street", "postcode", "place", "birthday"]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        # converting to string because form cannot handle date internationalization
        if self.instance and self.instance.id:
            self.initial['birthday'] = str(self.initial['birthday'])

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
