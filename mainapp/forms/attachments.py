from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row
from django import forms

from mainapp.models import Attachments, AttachmentTemplate


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachments
        fields = ['file_name', 'upload']

    def __init__(self, *args, **kwargs):
        self.customer_id = kwargs.pop("customer_id", None)
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.customer_id = self.customer_id
        if self.request:
            instance.uploaded_by = self.request.user
        instance.save()


class AttachmentTemplateForm(forms.ModelForm):
    class Meta:
        model = AttachmentTemplate
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-control'

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                *[Row(field_name, css_class='form-group')
                  for field_name in list(self.fields.keys())],
                css_class='col-md-12'
            )
        )
