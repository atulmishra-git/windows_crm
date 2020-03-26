from django import forms


class AddAttachmentsForm(forms.Form):
    file_type = forms.CharField(required=True,
                                max_length=1000,
                                widget=forms.TextInput(
                                      attrs={
                                          'class': 'form-control',
                                      }
                                ))
