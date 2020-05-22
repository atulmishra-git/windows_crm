from django.views.generic import TemplateView, CreateView, UpdateView, ListView
from django.utils.translation import ugettext_lazy as _

from mainapp.forms.add_manager import ManagerForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import User
from mainapp.permissions import IsSuperAdmin


class ListManagerView(IsSuperAdmin, ListView):
    template_name = 'managers/list_managers.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ManagerForm()
        return context


class CreateManagerView(IsSuperAdmin, CreateView):
    template_name = 'managers/list_managers.html'
    form_class = ManagerForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(CreateManagerView, self).get_context_data(**kwargs)
        context['operation'] = _("Add Manager")
        context['object_list'] = User.objects.all()
        return context

    def get_success_url(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return reverse('mainapp:new:list_manager', kwargs=dict())


class UpdateManagerView(IsSuperAdmin, UpdateView):
    template_name = 'managers/edit_manager.html'
    form_class = ManagerForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(UpdateManagerView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Manager")
        context['manager'] = str(self.object)
        return context

    def get_success_url(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return reverse('mainapp:new:list_manager', kwargs=dict())


def delete_manager(request, pk):
    try:
        user = request.user
        # check for superuser
        if not user.is_superuser:
            return redirect('mainapp:new:home')
        manager = User.fetch(user_id=pk)
        if manager:
            manager.delete()
        return redirect('mainapp:new:list_manager')
    except:
        return redirect('mainapp:new:list_manager')
