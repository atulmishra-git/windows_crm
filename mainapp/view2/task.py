from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.utils.translation import ugettext_lazy as _

from mainapp.forms.mixins import FormRequestMixin
from mainapp.forms.task import AddTaskForm
from django.shortcuts import reverse, redirect
from mainapp.models import Tasks, Customer


class IsCreatorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user != self.get_object().creator:
            return JsonResponse({'message': _('You are not permitted to perform the action.')})
        return super().dispatch(request, *args, **kwargs)


class IsCreatorOrSuperAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if request.user == self.get_object().creator:
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({'message': _('You are not permitted to perform the action.')})


class TasksView(LoginRequiredMixin, FormRequestMixin, ListView):
    template_name = 'tasks/list.html'
    form_class = AddTaskForm
    model = Tasks

    def filter_by_user(self, qs):
        if not self.request.user.is_superuser:
            return qs.filter(user=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(**dict(request=self.request))
        context['completed_list'] = self.filter_by_user(
            Tasks.objects.filter(completed=True)
        ).order_by('-todo_date')[:5]
        context['customer'] = Customer.objects.last()
        return context

    def get_queryset(self):
        qs = super().get_queryset().filter(
            completed=False).order_by('completed', 'todo_date')
        qs = self.filter_by_user(qs)
        return qs


class TaskCreateView(FormRequestMixin, CreateView):
    template_name = 'tasks/list.html'
    form_class = AddTaskForm
    model = Tasks

    def get_success_url(self):
        return reverse('mainapp:new:open_task_list', kwargs=dict())


class TaskUpdateView(IsCreatorMixin, FormRequestMixin, UpdateView):
    template_name = 'tasks/update.html'
    form_class = AddTaskForm
    model = Tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('mainapp:new:open_task_list', kwargs=dict())


class DeleteTaskView(IsCreatorOrSuperAdminMixin, DeleteView):
    model = Tasks

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:new:open_task_list', kwargs=dict())


def mark_completed(request, pk):
    task = Tasks.objects.get(pk=pk)
    try:
        user = request.user
        # check for superuser
        if user == task.creator or user == task.user or user.is_superuser:
            task.completed = True
            task.save()
        else:
            return JsonResponse({'messsage': _('You are not permitted to perform the action.')},
                                status=400)
    except:
        pass
    return redirect('mainapp:new:open_task_list')


@csrf_exempt
@login_required
def create_task(request):
    if request.method in ['POST', 'PATCH']:
        data = {}
        for k, v in request.POST.items():
            data.update({k: v})
        data['private'] = data['private'] == 'true'
        Tasks.objects.create(
            **data,
            user=request.user,
            creator=request.user,
        )
    return JsonResponse(data={}, status=200)
