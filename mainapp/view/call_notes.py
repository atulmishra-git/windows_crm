from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from mainapp.forms.call_notes import AddCallNotesForm
from mainapp.forms.mixins import FormRequestMixin
from mainapp.models import Customer, CallNotes


class CallNotesFormRequestMixin(object):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['customer_id'] = self.kwargs['customer_id']
        return kwargs


class CallNotesRedirectMixin:
    def get_success_url(self):
        return reverse('mainapp:add_call_notes', kwargs=dict(customer_id=self.kwargs['customer_id']))


class CallNotesCreateView(LoginRequiredMixin, CallNotesFormRequestMixin, CallNotesRedirectMixin, CreateView):
    template_name = 'call_notes.html'
    form_class = AddCallNotesForm
    model = CallNotes

    def get_context_data(self, **kwargs):
        context = super(CallNotesCreateView, self).get_context_data(**kwargs)
        customer = Customer.fetch(customer_id=self.kwargs['customer_id'])
        call_notes = CallNotes.fetch(customer_id=customer).order_by('-id')
        context.update(**{
            'customer_id': customer.id,
            'customer': customer,
            'object_list': call_notes
        })
        return context


class CallNotesUpdateView(LoginRequiredMixin, CallNotesFormRequestMixin, CallNotesRedirectMixin, UpdateView):
    template_name = 'call_notes.html'
    form_class = AddCallNotesForm
    model = CallNotes

    def get_context_data(self, **kwargs):
        context = super(CallNotesUpdateView, self).get_context_data(**kwargs)
        customer = Customer.fetch(customer_id=self.kwargs['customer_id'])
        context.update(**{
            'customer_id': customer.id,
            'customer': customer,
        })
        context['operation'] = 'Update'
        return context


class CallNotesDeleteView(LoginRequiredMixin, CallNotesRedirectMixin, DeleteView):
    model = CallNotes

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
