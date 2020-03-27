from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.generic import CreateView, UpdateView, DeleteView

from mainapp.forms.mixins import FormRequestMixin
from mainapp.forms.task import AddTaskForm
from django.shortcuts import reverse, redirect
from mainapp.models import Tasks


class IsCreatorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().creator:
            return JsonResponse({'message': 'You are not permitted to perform the action.'})
        return super().dispatch(request, *args, **kwargs)


class TasksView(LoginRequiredMixin, FormRequestMixin, CreateView):
    template_name = 'task_list.html'
    form_class = AddTaskForm
    model = Tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Tasks.objects.all().order_by('completed', 'todo_date')
        if not self.request.user.is_superuser:
            # only logged in users tasks
            tasks = tasks.filter(user=self.request.user)
        context['object_list'] = tasks
        context['operation'] = 'Create'
        return context

    def get_success_url(self):
        return reverse('mainapp:open_task_list', kwargs=dict())


class TaskUpdateView(IsCreatorMixin, FormRequestMixin, UpdateView):
    template_name = 'task_list.html'
    form_class = AddTaskForm
    model = Tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = 'Update'
        return context

    def get_success_url(self):
        return reverse('mainapp:open_task_list', kwargs=dict())


class DeleteTaskView(IsCreatorMixin, DeleteView):
    model = Tasks

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:open_task_list', kwargs=dict())


def mark_completed(request, pk):
    task = Tasks.objects.get(pk=pk)
    try:
        user = request.user
        # check for superuser
        if user == task.creator or user == task.user:

            task.completed = True
            task.save()
        else:
            return JsonResponse({'messsage': 'Action not permitted'},
                                status=400)
    except:
        pass
    return redirect('mainapp:open_task_list')
