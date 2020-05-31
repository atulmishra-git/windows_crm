import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.http.response import JsonResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from mainapp.forms.attachments import AttachmentForm, AttachmentTemplateForm
from django.shortcuts import render, reverse, redirect

from mainapp.forms.mixins import FormRequestMixin
from mainapp.models import Customer, Attachments, AttachmentTemplate
from mainapp.view.constants import ATTACHMENT_KINDS


class CustomerFormKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer_id'] = self.kwargs['customer_id']
        return kwargs


class AttachmentCreateView(CustomerFormKwargMixin, FormRequestMixin, LoginRequiredMixin, CreateView):
    template_name = 'attachments/list.html'
    model = Attachments
    form_class = AttachmentForm

    def get_form_kwargs(self):
        return super().get_form_kwargs()

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
        return reverse('mainapp:new:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


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
        return reverse('mainapp:new:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


class DeleteAttachmentView(LoginRequiredMixin, DeleteView):
    model = Attachments

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('mainapp:new:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


@login_required
def email_attachment(request, customer_id, pk):
    attachment = Attachments.objects.get(customer_id=customer_id, pk=pk)
    try:
        kind = ATTACHMENT_KINDS[attachment.kind]
        template = AttachmentTemplate.objects.get(kind=kind)
        subject = template.subject
        text_content = template.body
    except KeyError:
        subject = ''
        text_content = ''
    to = attachment.customer.email
    from_email = settings.EMAIL_HOST_USER
    # html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    msg.attach_file(os.path.join(settings.MEDIA_ROOT, attachment.upload.name))
    msg.send()
    return redirect(reverse('mainapp:new:home'))


class UpdateAttachmentTemplateView(LoginRequiredMixin, View):
    template_name = 'attachment_settings/index.html'
    form_class = AttachmentTemplateForm
    model = AttachmentTemplate

    def get(self, request, *args, **kwargs):
        templates = AttachmentTemplate.objects.get
        context = {
            'offer_form': self.form_class(instance=templates(kind='offer')),
            'offer_confirmation_form': self.form_class(instance=templates(kind='offer_confirmation')),
            'install_form': self.form_class(instance=templates(kind='install')),
            'invoice_form': self.form_class(instance=templates(kind='invoice')),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        kind = data.pop('kind')[0]
        form = self.form_class(instance=AttachmentTemplate.objects.get(kind=kind), data=data)
        if form.is_valid():
            form.save()
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({}, status=400)
