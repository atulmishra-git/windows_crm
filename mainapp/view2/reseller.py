from django.views.generic import CreateView, UpdateView, ListView
from django.utils.translation import ugettext_lazy as _

from mainapp.forms.reseller import ResellerForm
from django.shortcuts import redirect, reverse
from mainapp.models import Reseller
from mainapp.permissions import IsSuperAdmin


class ListObjectsView(IsSuperAdmin, ListView):
    template_name = 'reseller/list_reseller.html'
    model = Reseller

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResellerForm()
        return context


class CreateObjectView(IsSuperAdmin, CreateView):
    template_name = 'reseller/list_reseller.html'
    form_class = ResellerForm
    model = Reseller

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['operation'] = _("Add Reseller")
        context['object_list'] = Reseller.objects.all()
        return context

    def get_success_url(self):
        return reverse('mainapp:new:list_reseller', kwargs=dict())


class UpdateObjectView(IsSuperAdmin, UpdateView):
    template_name = 'reseller/edit_reseller.html'
    form_class = ResellerForm
    model = Reseller

    def get_context_data(self, **kwargs):
        context = super(UpdateObjectView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Reseller")
        context['object'] = str(self.object)
        return context

    def get_success_url(self):
        return reverse('mainapp:new:list_reseller', kwargs=dict())


def delete(request, pk):
    try:
        reseller = Reseller.objects.get(id=pk)
        if reseller:
            reseller.delete()
        return redirect('mainapp:new:list_reseller')
    except:
        return redirect('mainapp:new:list_reseller')
