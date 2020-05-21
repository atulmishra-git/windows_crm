from django import forms

from mainapp.forms.mixins import LabelAdder
from mainapp.models import Customer, GENDER_CHOICES, PURPOSE_CHOICES


class CustomerForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['purpose', 'gender', 'first_name', 'surname', 'offer_id', 'invoice_id', 'street',
                  'place', 'postcode', 'phone', 'mobile', 'email', 'birthday']
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
