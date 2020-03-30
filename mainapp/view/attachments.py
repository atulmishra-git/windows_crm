from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from mainapp.forms.attachments import AttachmentForm
from django.shortcuts import render, reverse

from mainapp.forms.mixins import FormRequestMixin
from mainapp.models import Customer, Attachments


class CustomerFormKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer_id'] = self.kwargs['customer_id']
        return kwargs


class AttachmentCreateView(CustomerFormKwargMixin, FormRequestMixin, LoginRequiredMixin, CreateView):
    template_name = 'attachments.html'
    model = Attachments
    form_class = AttachmentForm

    def get_context_data(self, **kwargs):
        customer_id = self.kwargs['customer_id']
        attachments = Attachments.objects.filter(customer_id=customer_id).order_by('-id')
        cxt = super().get_context_data(**kwargs)
        cxt.update({
            'customer_id': customer_id,
            'object_list': attachments
        })
        return cxt

    def get_success_url(self):
        return reverse('mainapp:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


class UpdateAttachmentView(CustomerFormKwargMixin, LoginRequiredMixin, UpdateView):
    template_name = 'attachments.html'
    form_class = AttachmentForm
    model = Attachments

    def get_context_data(self, **kwargs):
        context = super(UpdateAttachmentView, self).get_context_data(**kwargs)
        context['operation'] = "Update"
        context['customer_id'] = self.kwargs['customer_id']
        return context

    def get_success_url(self):
        return reverse('mainapp:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


class DeleteAttachmentView(LoginRequiredMixin, DeleteView):
    model = Attachments

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))
