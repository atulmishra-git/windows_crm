from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import reverse
from mainapp.forms.add_purchase_record import PurchaseRecordForm
from mainapp.models import PurchaseRecord
from mainapp.permissions import IsSuperAdmin


class AddPurchaseView(CreateView):
    template_name = 'add_purchase.html'
    form_class = PurchaseRecordForm
    model = PurchaseRecord

    def get_success_url(self):
        return reverse('mainapp:list_purchase', kwargs=dict())


class ListPurchaseView(ListView):
    template_name = 'list_purchase.html'
    model = PurchaseRecord

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['object_type'] = 'Purchase'
        return context


class UpdatePurchaseView(UpdateView):
    template_name = 'add_purchase.html'
    form_class = PurchaseRecordForm
    model = PurchaseRecord

    def get_context_data(self, **kwargs):
        context = super(UpdatePurchaseView, self).get_context_data(**kwargs)
        context['operation'] = "Update"
        return context

    def get_success_url(self):
        return reverse('mainapp:list_purchase', kwargs=dict())


class DeletePurchaseView(IsSuperAdmin, DeleteView):
    model = PurchaseRecord

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:list_purchase', kwargs=dict())
