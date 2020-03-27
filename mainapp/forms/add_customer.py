from django import forms

from mainapp.forms.mixins import LabelAdder
from mainapp.models import Customer, GENDER_CHOICES, PURPOSE_CHOICES


class CustomerForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'surname', 'offer_id', 'invoice_id', 'street', 'postcode', 'place', 'phone', 'mobile', 'email']

    # gender = forms.ChoiceField(required=True,
    #                            choices=GENDER_CHOICES,
    #                            widget=forms.Select({
    #                                'class': 'form-control'
    #                            }))
