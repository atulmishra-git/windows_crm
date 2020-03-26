from django import forms


class AddCallNotesForm(forms.Form):
    notes = forms.CharField(required=True,
                            max_length=1000,
                            widget=forms.Textarea(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Notes',
                                      'rows': '4'
                                  }
                            ))
