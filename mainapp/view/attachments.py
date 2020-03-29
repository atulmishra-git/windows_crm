from django.views.generic import TemplateView, CreateView
from mainapp.forms.attachments import AddAttachmentsForm, AttachmentForm
from django.shortcuts import render, reverse
from mainapp.models import Customer, Attachments
from django.http import JsonResponse
from mainapp.gc_storage import save_file


class CustomerFormKwargMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer_id'] = self.kwargs['customer_id']
        return kwargs


class AttachmentCreateView(CustomerFormKwargMixin, CreateView):
    template_name = 'attachments.html'
    model = Attachments
    form_class = AttachmentForm

    def get_context_data(self, **kwargs):
        customer = Customer.objects.get(id=self.kwargs['customer_id'])
        attachments = customer.attachments.all()
        cxt = super().get_context_data(**kwargs)
        cxt.update({
            'customer': customer,
            'attachments': attachments
        })
        return cxt

    def get_success_url(self):
        return reverse('mainapp:add_attachments', kwargs=dict(customer_id=self.kwargs['customer_id']))


class AttachmentsView(TemplateView):
    template_name = 'attachments.html'

    def get(self, request, customer_id, *args, **kwargs):
        add_attachment_form = AddAttachmentsForm()

        customer = Customer.fetch(customer_id=customer_id)
        attachments = Attachments.fetch(customer_id=customer_id)

        context = {
            'add_attachment': add_attachment_form,
            'customer_id': customer_id,
            'customer': customer,
            'attachments': attachments
        }
        return render(request, self.template_name, context=context)

    def post(self, request, customer_id):
        try:
            customer_id = request.POST.get('customer_id')
            image = request.FILES.get('upload_file')
            add_attachment_form = AddAttachmentsForm(request.POST)
            user_id = request.user.id

            if add_attachment_form.is_valid():
                file_type = add_attachment_form.cleaned_data.get('file_type')
                public_url = ''

                public_url = save_file(image)

                create_attachment = Attachments.create(customer_id=customer_id, file_type=file_type,
                                                       file_link=public_url)
                if create_attachment:
                    return JsonResponse({
                        'success': True,
                    })

                return JsonResponse({
                    'success': False,
                    'message': "Can't create the call note. Please try again"
                })

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please Fill All the Fields.'
                })

        except Exception as e:
            print("Exception occurs in Creating Attachments View. Error: {}".format(str(e)))
            return JsonResponse({
                'success': False,
                'message': "Something went wrong. Please Try Again!"
            })
