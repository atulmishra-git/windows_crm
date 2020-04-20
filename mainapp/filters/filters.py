import django_filters

from mainapp.models import Customer


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
