from django import forms
from mainapp.models import User


class AddTaskForm(forms.Form):
    user = forms.ModelChoiceField(required=True,
                                  queryset=User.fetch(),
                                  widget=forms.Select(
                                      attrs={
                                           'class': 'form-control',
                                      }
                                  ))
    message = forms.CharField(required=True,
                              max_length=1000,
                              widget=forms.Textarea(
                                 attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Task'
                                 }
                              ))
