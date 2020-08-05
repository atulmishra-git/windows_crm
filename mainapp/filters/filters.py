import django_filters
from django import forms
from django.db import models
from django.db.models.fields import DateField
from django.forms.widgets import DateInput

from mainapp.models import Customer, PurchaseRecord


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'first_name': ['icontains'],
            'surname': ['icontains'],
            'offer_id': ['iexact'],
            'invoice_id': ['iexact'],
            'street': ['icontains'],
            'place': ['icontains'],
            'phone': ['iexact'],
            'mobile': ['iexact'],
            'email': ['iexact']
        }


class PurchaseFilter(django_filters.FilterSet):
    class Meta:
        model = PurchaseRecord
        fields = {
            'customer__id': ['exact'],
            'dc_term': ['gte', 'lt'],
            'dc_mechanic': ['exact'],
            'ac_term': ['gte', 'lt'],
            'ac_mechanic': ['exact'],
            'reseller_name': ['exact']
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date'})
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print()
