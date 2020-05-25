from django import forms
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError
from django.forms.widgets import SelectDateWidget

from mainapp.models import Tasks


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['user', 'message', 'todo_date', 'todo_time', 'private']
        widgets = {
            'todo_date': forms.DateInput(attrs={'type': 'date'}),
            'todo_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        for field_name in self.fields.keys():
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        # converting to string because form cannot handle date internationalization
        if self.instance and self.instance.id:
            self.initial['todo_date'] = str(self.initial['todo_date'])
        if not self.request.user.is_superuser:
            self.fields['user'].queryset = self.fields['user'].queryset.filter(
                pk=self.request.user.pk
            )

    def clean_todo_date(self):
        value = self.cleaned_data['todo_date']
        if not value:
            raise forms.ValidationError('Bad Date')
        return value

    def clean_todo_time(self):
        value = self.cleaned_data['todo_time']
        if not value:
            raise forms.ValidationError('Bad Time')
        return value

    def save(self, commit=True):
        instance = super(AddTaskForm, self).save(commit=commit)
        if self.request:
            instance.creator = self.request.user
            instance.save()
