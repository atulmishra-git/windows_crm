from django.views.generic import CreateView, UpdateView, ListView
from django.utils.translation import ugettext_lazy as _

from mainapp.forms.mechanic import MechanicForm
from django.shortcuts import redirect, reverse
from mainapp.models import Mechanic, Customer
from mainapp.permissions import IsSuperAdmin


class ListObjectsView(IsSuperAdmin, ListView):
    template_name = 'mechanic/list_mechanic.html'
    model = Mechanic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MechanicForm()
        context['customer'] = Customer.objects.last()
        return context


class CreateObjectView(IsSuperAdmin, CreateView):
    template_name = 'mechanic/list_mechanic.html'
    form_class = MechanicForm
    model = Mechanic

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['operation'] = _("Add Mechanic")
        context['object_list'] = Mechanic.objects.all()
        return context

    def get_success_url(self):
        return reverse('mainapp:new:list_mechanic', kwargs=dict())


class UpdateObjectView(IsSuperAdmin, UpdateView):
    template_name = 'mechanic/edit_mechanic.html'
    form_class = MechanicForm
    model = Mechanic

    def get_context_data(self, **kwargs):
        context = super(UpdateObjectView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Mechanic")
        context['object'] = str(self.object)
        return context

    def get_success_url(self):
        return reverse('mainapp:new:list_mechanic', kwargs=dict())


def delete(request, pk):
    try:
        mechanic = Mechanic.objects.get(id=pk)
        if mechanic:
            mechanic.delete()
        return redirect('mainapp:new:list_mechanic')
    except:
        return redirect('mainapp:new:list_mechanic')
