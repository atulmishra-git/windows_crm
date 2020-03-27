from django import forms
from mainapp.models import Tasks


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['user', 'message', 'todo_date', 'completed']
