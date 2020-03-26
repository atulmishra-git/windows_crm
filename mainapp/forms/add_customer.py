from django import forms
from mainapp.models import Customer, GENDER_CHOICES, PURPOSE_CHOICES


class AddCustomerForm(forms.Form):
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
    mobile = forms.CharField(required=True,
                             max_length=255,
                             widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Mobile Number'
                                }
                             ))
    place = forms.CharField(required=True,
                            max_length=255,
                            widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Place'
                                 }
                            ))
    street = forms.CharField(required=True,
                             max_length=255,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Email'
                                 }
                             ))
    postcode = forms.CharField(required=True,
                               max_length=255,
                               widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'postcode'
                                 }
                               ))
    gender = forms.ChoiceField(required=True,
                               choices=GENDER_CHOICES,
                               widget=forms.Select({
                                   'class': 'form-control'
                               }))
    purpose = forms.ChoiceField(required=True,
                                choices=PURPOSE_CHOICES,
                                widget=forms.Select({
                                   'class': 'form-control'
                                }))

    def clean(self):
        cleaned_data = super().clean()

        cc_phone = self.cleaned_data.get('phone')
        cc_mobile = self.cleaned_data.get('mobile')

        try:
            user_phone = Customer.objects.get(phone=cc_phone)
        except Customer.DoesNotExist:
            user_phone = None

        if user_phone:
            self.add_error('phone', "Already taken")
            return cleaned_data

        try:
            user_mobile = Customer.objects.get(mobile=cc_mobile)
        except Customer.DoesNotExist:
            user_mobile = None

        if user_mobile:
            self.add_error('mobile', "Already taken")
            return cleaned_data

        return cleaned_data
