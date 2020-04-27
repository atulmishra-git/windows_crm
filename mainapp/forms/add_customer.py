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
