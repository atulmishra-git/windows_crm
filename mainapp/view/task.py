from django.views.generic import TemplateView
from mainapp.forms.task import AddTaskForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from mainapp.models import Tasks, User


class TasksView(TemplateView):
    template_name = 'task_list.html'

    def get(self, request, *args, **kwargs):
        add_task_form = AddTaskForm()
        if request.user.is_superuser:
            tasks_list = Tasks.fetch()
        else:
            tasks_list = Tasks.fetch(request.user.id)

        context = {
            'add_task_form': add_task_form,
            'tasks': tasks_list
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        add_task_form = AddTaskForm(request.POST)

        if add_task_form.is_valid():
            user = add_task_form.cleaned_data.get('user')
            message = add_task_form.cleaned_data.get('message')

            task = Tasks.create(user_id=user.id, message=message)

            if task:
                return JsonResponse({
                    'success': True
                })

            return JsonResponse({
                'success': False,
                'message': 'Error in Assigning Tasks'
            })

        return JsonResponse({
            'success': False,
            'message': 'Please Fill All the Fields'
        })
