from django import forms
from mainapp.models import Tasks


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['user', 'message', 'todo_date', 'completed']
        widgets = {
            'todo_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AddTaskForm, self).save(commit=commit)
        if self.request:
            instance.creator = self.request.user
            instance.save()
