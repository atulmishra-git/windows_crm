from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _

from mainapp.filters.filters import PurchaseFilter
from mainapp.forms.add_purchase_record import PurchaseRecordForm
from mainapp.models import PurchaseRecord
from mainapp.permissions import IsSuperAdmin
from mainapp.view.mixins import FilterListMixin


@csrf_exempt
@login_required
def update_purchase(request, pk):
    count = 0
    if request.method in ['POST', 'PATCH']:
        # only one pair of k, v is received
        for k, v in request.POST.items():
            count = PurchaseRecord.objects.filter(pk=pk).update(**{k: v})
    return JsonResponse(data={'message': f'{count} purchases updated'}, status=200)


class AddPurchaseView(LoginRequiredMixin, CreateView):
    template_name = 'purchases/add_update_purchase.html'
    form_class = PurchaseRecordForm
    model = PurchaseRecord

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operation'] = _("Add Purchase")
        return context

    def form_invalid(self, form):
        response = super(AddPurchaseView, self).form_invalid(form)
        return response

    def get_success_url(self):
        messages.success(self.request,
                         _("Purchase added successfully."))
        return reverse('mainapp:new:list_purchase', kwargs=dict())


class ListPurchaseView(LoginRequiredMixin, FilterListMixin, ListView):
    template_name = 'purchases/list_purchases.html'
    filterset_class = PurchaseFilter
    model = PurchaseRecord
    # paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['object_type'] = _('Purchase')
        return context


class UpdatePurchaseView(LoginRequiredMixin, UpdateView):
    template_name = 'purchases/add_update_purchase.html'
    form_class = PurchaseRecordForm
    model = PurchaseRecord

    def get_context_data(self, **kwargs):
        context = super(UpdatePurchaseView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Purchase")
        return context

    def get_success_url(self):
        messages.add_message(self.request,
                             messages.SUCCESS,
                             _("Purchase updated successfully."))
        return reverse('mainapp:new:list_purchase', kwargs=dict())


class DeletePurchaseView(IsSuperAdmin, DeleteView):
    model = PurchaseRecord

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:list_purchase', kwargs=dict())
