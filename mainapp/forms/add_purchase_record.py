from django import forms
from mainapp.models import Customer


class AddPurchaseRecordForm(forms.Form):
    customer = forms.ModelChoiceField(required=True,
                                      queryset=Customer.fetch(),
                                      widget=forms.Select(
                                          attrs={
                                              'class': 'form-control'
                                          }
                                      ))
    reseller_name = forms.CharField(required=True,
                                    max_length=255,
                                    widget=forms.TextInput(
                                         attrs={
                                             'class': 'form-control',
                                             'placeholder': 'Reseller Name'
                                         }
                                    ))
    module_count = forms.CharField(required=True,
                                   max_length=255,
                                   widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Module Count'
                                        }
                                   ))
    module_type = forms.CharField(required=True,
                                  max_length=255,
                                  widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Module Type'
                                        }
                                  ))
    memory_type = forms.CharField(required=True,
                                  max_length=255,
                                  widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Memory Type'
                                        }
                                  ))
    kwp = forms.CharField(required=True,
                          max_length=255,
                          widget=forms.TextInput(
                            attrs={
                                'class': 'form-control',
                                'placeholder': 'kwp'
                            }
                          ))
    price_without_tax = forms.CharField(required=True,
                                        max_length=255,
                                        widget=forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Price Without Tax'
                                            }
                                        ))
    price_with_tax = forms.CharField(required=True,
                                     max_length=255,
                                     widget=forms.TextInput(
                                        attrs={
                                            'class': 'form-control',
                                            'placeholder': 'Price With Tax'
                                        }
                                     ))
    offer_created = forms.BooleanField(required=False)
    cancellation = forms.BooleanField(required=False)
    project_planning_created = forms.BooleanField(required=False)
    installation_date = forms.DateField(required=True,
                                        widget=forms.DateInput(
                                            attrs={
                                                'type': 'date',
                                                'class': 'form-control',
                                            }
                                        ))
    ac_date = forms.DateField(required=True,
                              widget=forms.DateInput(
                                attrs={
                                    'type': 'date',
                                    'class': 'form-control',
                                }
                              ))
    photo_roof_access = forms.BooleanField(required=False)
    photo_counter_cabinet = forms.BooleanField(required=False)
    video_counter = forms.BooleanField(required=False)
    photo_of_counter = forms.BooleanField(required=False)
    power_of_attorney = forms.BooleanField(required=False)
    data_collection = forms.BooleanField(required=False)
    order_date = forms.DateField(required=True,
                                 widget=forms.DateInput(
                                    attrs={
                                        'type': 'date',
                                        'class': 'form-control',
                                    }
                                 ))
    with_battery = forms.BooleanField(required=False)
