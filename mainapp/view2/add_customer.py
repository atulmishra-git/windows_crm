from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView

from mainapp.filters.filters import CustomerFilter
from mainapp.forms.add_customer import CustomerForm
from mainapp.models import Customer
from mainapp.view.mixins import FilterListMixin


@csrf_exempt
@login_required
def update_customer(request, pk):
    if request.method in ['POST', 'PATCH']:
        # only one pair of k, v is received
        for k, v in request.POST.items():
            Customer.objects.filter(pk=pk).update(**{k: v})
    return JsonResponse(data={}, status=200)


class AddCustomerView(LoginRequiredMixin, CreateView):
    template_name = 'customer/add_customer.html'
    form_class = CustomerForm
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(AddCustomerView, self).get_context_data(**kwargs)
        context['operation'] = _("Add New Customer")
        context['fields'] = list(self.form_class.base_fields.keys())
        return context

    def get_success_url(self):
        messages.success(self.request,
                         _("Customer added successfully."))
        return reverse('mainapp:list_customer', kwargs=dict())


class UpdateCustomerView(LoginRequiredMixin, UpdateView):
    template_name = 'customer/add_customer.html'
    form_class = CustomerForm
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(UpdateCustomerView, self).get_context_data(**kwargs)
        context['operation'] = _("Update Customer")
        context['fields'] = list(self.form_class.base_fields.keys())
        return context

    def get_success_url(self):
        messages.success(self.request,
                         _("Customer updated successfully."))
        return reverse('mainapp:list_customer', kwargs=dict())


class ListCustomerView(LoginRequiredMixin, FilterListMixin, ListView):
    template_name = 'customer/list_customer.html'
    filterset_class = CustomerFilter
    model = Customer
    paginate_by = 10


class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = Customer

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:add_customer', kwargs=dict())
