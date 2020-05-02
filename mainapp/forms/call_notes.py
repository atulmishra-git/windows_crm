from django import forms

from mainapp.forms.mixins import LabelAdder
from mainapp.models import CallNotes


class AddCallNotesForm(LabelAdder, forms.ModelForm):
    class Meta:
        model = CallNotes
        fields = ['notes', 'status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.customer_id = kwargs.pop("customer_id", None)
        if not self.request or not self.customer_id:
            raise AttributeError("request missing")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddCallNotesForm, self).save(commit=False)
        instance.user = self.request.user
        instance.customer_id = self.customer_id
        instance.save()
