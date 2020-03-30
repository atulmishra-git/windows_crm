import pdfkit
from django.template.context import RequestContext
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.conf import settings

from mainapp.models import Customer, PurchaseRecord, Attachments
from mainapp.utils import render_to_pdf


class InvoicesView(TemplateView):
    template_name = 'invoice.html'

    def get(self, request, customer_id, *args, **kwargs):
        purchase_records = PurchaseRecord.fetch(customer_id=customer_id)
        customer = Customer.fetch(customer_id=customer_id)

        context = {
            'customer_id': customer_id,
            'customer': customer,
            'purchases': purchase_records
        }
        return render(request, self.template_name, context=context)


def download_invoice(request, purchase_id):
    # template = get_template('pdf/invoice.html')
    purchase = PurchaseRecord.objects.last(purchase_id=purchase_id)
    if not purchase:
        return HttpResponse(status=404)
    customer = purchase.customer

    p = {
        'id': purchase.id,
        'name': purchase.customer.first_name + ' ' + purchase.customer.surname,
        'customer_id': customer.id,
        'fullname': f'{"Mr. " if customer.gender == "Male" else "Ms. "}{str(customer)}',
        'street': customer.street,
        'postcode': customer.postcode,
        'place': customer.place,
        'offer_date': purchase.offer_date,
        'date_sent': purchase.date_sent,
        'price_without_tax': purchase.price_without_tax,
        'tax': "%0.2f" % (purchase.price_without_tax * 0.19),
        'price_with_tax': purchase.price_with_tax,
    }
    context = {
        'purchase': p
    }

    rendered = render_to_string('pdf/invoice.html',
                                context,
                                request=request)
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdf = pdfkit.from_string(rendered, False, options=options)
    return HttpResponse(pdf, content_type="application/pdf")
