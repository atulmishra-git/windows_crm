from django.shortcuts import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from mainapp.forms.add_customer import CustomerForm
from mainapp.models import Customer
from mainapp.view.mixins import RedirectToHome


class AddCustomerView(CreateView):
    template_name = 'add_customer.html'
    form_class = CustomerForm
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(AddCustomerView, self).get_context_data(**kwargs)
        context['operation'] = "Add New"
        context['object_type'] = "Customer"
        context['fields'] = list(self.form_class.base_fields.keys())
        context['objects'] = Customer.objects.order_by('-id').values('id', *context['fields'])
        return context

    def get_success_url(self):
        return reverse('mainapp:add_customer', kwargs=dict())


class UpdateCustomerView(UpdateView):
    template_name = 'add_customer.html'
    form_class = CustomerForm
    model = Customer

    def get_context_data(self, **kwargs):
        context = super(UpdateCustomerView, self).get_context_data(**kwargs)
        context['operation'] = "Update"
        context['object_type'] = "Customer"
        context['fields'] = list(self.form_class.base_fields.keys())
        context['objects'] = Customer.objects.values('id', *context['fields'])
        return context

    def get_success_url(self):
        return reverse('mainapp:add_customer', kwargs=dict())


class DeleteCustomerView(DeleteView):
    model = Customer

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:add_customer', kwargs=dict())
