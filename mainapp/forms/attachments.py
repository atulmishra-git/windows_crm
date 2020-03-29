from django import forms

from mainapp.models import Attachments


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachments
        fields = ['file_name', 'upload']

    def __init__(self, *args, **kwargs):
        self.customer_id = kwargs.pop("customer_id", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.customer_id = self.customer_id
        instance.save()
