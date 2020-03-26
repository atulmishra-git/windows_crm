from django import forms


class SearchForm(forms.Form):
    name = forms.CharField(required=True,
                           max_length=255,
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Search by Customer Name'
                               }
                           ))
