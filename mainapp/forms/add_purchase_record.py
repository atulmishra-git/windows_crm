from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


from mainapp.forms.mixins import LabelAdder
from mainapp.models import Customer, PurchaseRecord


class PurchaseRecordForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = PurchaseRecord
        exclude = ['created_at', 'is_active']
        widgets = {
            'offer_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'date_sent': forms.DateTimeInput(attrs={'type': 'date'}),
            'dc_term': forms.DateTimeInput(attrs={'type': 'date'}),
            'ac_term': forms.DateTimeInput(attrs={'type': 'date'}),
            'installation_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('customer', css_class='form-group col-md-6 mb-0'),
                Column('manufacturer', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'with_battery',
            Row(
                Column('watt', css_class='form-group col-md-4 mb-0'),
                Column('kwp', css_class='form-group col-md-4 mb-0'),
                Column('price_without_tax', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            'offer_by',
            Row(
                Column('offer_date', css_class='form-group col-md-6 mb-0'),
                Column('reseller_name', css_class='form-group col-md-4 mb-0'),
                Column('declined', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date_sent', css_class='form-group col-md-6 mb-0'),
                Column('project_planning_created', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('dc_term', css_class='form-group col-md-4 mb-0'),
                Column('dc_mechanic', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ac_term', css_class='form-group col-md-4 mb-0'),
                Column('ac_mechanic', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'roof_type',
            Row(
                Column('roof_tilt', css_class='form-group col-md-4 mb-0'),
                Column('alignment', css_class='form-group col-md-4 mb-0'),
                Column('module_area', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('module_type', css_class='form-group col-md-4 mb-0'),
                Column('memory_type', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('installation_date', css_class='form-group col-md-4 mb-0'),
                Column('cancellation', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Sign in')
        )
