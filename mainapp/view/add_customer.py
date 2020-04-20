from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.list import ListView

from mainapp.forms.add_customer import CustomerForm
from mainapp.models import Customer
from mainapp.view.mixins import RedirectToHome


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
        return reverse('mainapp:list_customer', kwargs=dict())


class ListCustomerView(LoginRequiredMixin, ListView):
    template_name = 'customer/list_customer.html'
    model = Customer
    paginate_by = 10


class DeleteCustomerView(LoginRequiredMixin, DeleteView):
    model = Customer

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:add_customer', kwargs=dict())
