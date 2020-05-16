from django.views.generic import TemplateView, CreateView, UpdateView
from django.utils.translation import ugettext_lazy as _

from mainapp.forms.add_manager import ManagerForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import User
from mainapp.permissions import IsSuperAdmin


class CreateManagerView(IsSuperAdmin, CreateView):
    template_name = 'add_manager.html'
    form_class = ManagerForm
    model = User

    def get_context_data(self, **kwargs):
        managers_list = User.fetch()
        context = super(CreateManagerView, self).get_context_data(**kwargs)
        context['operation'] = _("Add Manager")
        context['managers'] = managers_list
        return context

    def get_success_url(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return reverse('mainapp:add_manager', kwargs=dict())


class UpdateManagerView(IsSuperAdmin, UpdateView):
    template_name = 'add_manager.html'
    form_class = ManagerForm
    model = User

    def get_context_data(self, **kwargs):
        managers_list = User.fetch()
        context = super(UpdateManagerView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Manager")
        context['manager'] = str(self.object)
        context['managers'] = managers_list
        return context

    def get_success_url(self):
        self.object.set_password(self.object.password)
        self.object.save()
        return reverse('mainapp:add_manager', kwargs=dict())


def delete_manager(request, manager_id):
    try:
        user = request.user
        # check for superuser
        if not user.is_superuser:
            return redirect('mainapp:add_manager')
        manager = User.fetch(user_id=manager_id)
        if manager:
            manager.delete()
        return redirect('mainapp:add_manager')
    except:
        return redirect('mainapp:add_manager')

