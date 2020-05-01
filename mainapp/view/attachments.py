import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.views.generic import CreateView, UpdateView, DeleteView
from mainapp.forms.attachments import AttachmentForm
from django.shortcuts import render, reverse, redirect

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
        context['operation'] = "Update Attachment"
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


@login_required
def email_attachment(request, customer_id, pk):
    attachment = Attachments.objects.get(customer_id=customer_id, pk=pk)
    to = attachment.customer.email
    to = 'ann.shress@gmail.com'
    subject, from_email = '', settings.EMAIL_HOST_USER
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.upload.name))
    msg.send()
    return redirect(reverse('mainapp:home'))
