from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML

from mainapp.forms.mixins import LabelAdder
from mainapp.models import PurchaseRecord


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
                Column('customer', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            HTML('<h3>Module</h3>'),
            # Row(
            #     Column('manufacturer', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            Row(
                Column('watt', css_class='form-group col-md-4 mb-0'),
                Column('module_count', css_class='form-group col-md-4 mb-0'),
                HTML('<p>'
                     'KWP:  <strong><div id="id_kwp"></div></strong>'
                     '</p>'
                     '<br/>'),
                css_class='form-row'
            ),
            HTML('<h3>Choose if there is battery system or not</h3>'),
            'with_battery',
            HTML('<h3>With Battery</h3>'),
            Row(
                Column('manufacturer', css_class='form-group col-md-6 mb-0'),
                Column('kwh', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML('<h3>WR - Without Battery</h3>'),
            Row(
                Column('manufacturer2', css_class='form-group col-md-6 mb-0'),
                Column('kwh2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML('<h3>Price</h3>'),
            'price_without_tax',
            HTML('<p>Tax: 19%'
                 # '<br/>'
                 # 'Price With Tax: <div id="total_price"></div></p>'
                 '<br/>'),
            'offer_by',
            HTML('<h4>Offer Details</h4><br/>'),
            Row(
                Column('offer_date', css_class='form-group col-md-4 mb-0'),
                Column('reseller_name', css_class='form-group col-md-6 mb-0'),
                Column('declined', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            HTML('<h4>Technical Details</h4><br/>'),
            Row(
                Column('date_sent', css_class='form-group col-md-6 mb-0'),
                Column('project_planning_created', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('dc_term', css_class='form-group col-md-6 mb-0'),
                Column('dc_mechanic', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('ac_term', css_class='form-group col-md-6 mb-0'),
                Column('ac_mechanic', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML('<h4>Information of the Roof</h4><br/>'),
            'roof_type',
            Row(
                Column('roof_tilt', css_class='form-group col-md-4 mb-0'),
                Column('alignment', css_class='form-group col-md-4 mb-0'),
                Column('module_area', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('', css_class='form-group col-md-4 mb-0'),
                Column('', css_class='form-group col-md-4 mb-0'),
                HTML('<p>'
                     'Total Area of all modules: <div id="total_area"></div>'
                     '</p>'
                     '<br/>'),
                css_class='form-row'
            ),
            'extra_details',
            Submit('submit', 'Submit')
        )
