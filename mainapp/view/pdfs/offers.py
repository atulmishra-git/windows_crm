from datetime import datetime
import time
import pdfkit
from django.contrib.auth.decorators import login_required

from django.core.files.base import File
from django.http.response import HttpResponse
from django.template.loader import render_to_string

from mainapp.models import PurchaseRecord, Customer, Attachments

WATT1 = 310
WATT2 = 325
OPTIONS = {
    'page-size': 'A4',
    'margin-top': '0.7842in',
    'margin-right': '0.9842in',
    'margin-bottom': '0.7842in',
    'margin-left': '0.9842in',
    'encoding': "UTF-8",
    'no-outline': None
}


def save_to_attachment(customer, rendered, by):
    return
    name = f"uploads/{customer.id}offer{int(time.time())}.pdf"
    pdfkit.from_string(rendered, "media/" + name, options=OPTIONS)
    att = Attachments.objects.create(file_name=name.split("/")[-1].split(".")[0],
                                     uploaded_by=by,
                                     customer_id=customer.id)
    att.upload.name = name
    att.save()


@login_required
def download_offer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record
    if purchase.watt == WATT1:
        template_name = 'pdf/offer1.html'
    else:
        template_name = 'pdf/offer2.html'

    context = {
        'gender': "Mr" if customer.gender == 'Male' else "Ms",
        'customer': customer,
        'creator': request.user,
        'creation_date': datetime.today(),
    }

    rendered = render_to_string(template_name,
                                context,
                                request=request)
    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, rendered=rendered, by=request.user)
    return HttpResponse(pdf, content_type="application/pdf")


def download_offer_confirm(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record
    if purchase.watt == WATT1:
        template_name = 'pdf/offer_confirm1.html'
    else:
        template_name = 'pdf/offer_confirm2.html'

    # context = {
    #     'gender': "Mr" if customer.gender == 'Male' else "Ms",
    #     'name': str(customer),
    #     'customer_id': customer.id,
    #     'street': customer.street,
    #     'postcode': customer.postcode,
    #     'place': customer.place,
    #     'last_name': customer.surname,
    #     'creation_date': datetime.today(),
    # }
    context = {
        'mrms': "Mr",
        'name': "Denis Ibrahimi",
        'customer_id': 10299,
        'street': "Bayern Munchen",
        'postcode': "8920",
        'place': "4th Block, Sunshine Street",
        'last_name': "Ibrahimi",
        'creation_date': datetime.today(),
    }

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, rendered=rendered, by=request.user)
    return HttpResponse(pdf, content_type="application/pdf")


def download_install(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record
    template_name = 'pdf/install.html'

    # context = {
    #     'gender': "Mr" if customer.gender == 'Male' else "Ms",
    #     'name': str(customer),
    #     'customer_id': customer.id,
    #     'street': customer.street,
    #     'postcode': customer.postcode,
    #     'place': customer.place,
    #     'last_name': customer.surname,
    #     'creation_date': datetime.today(),
    # }
    context = {
        'mrms': "Mr",
        'name': "Denis Ibrahimi",
        'customer_id': 10299,
        'street': "Bayern Munchen",
        'postcode': "8920",
        'place': "4th Block, Sunshine Street",
        'last_name': "Ibrahimi",
        'creation_date': datetime.today(),
    }

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, rendered=rendered, by=request.user)
    return HttpResponse(pdf, content_type="application/pdf")


def download_invoice(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record
    template_name = 'pdf/invoice.html'

    context = {}
    #     'gender': "Mr" if customer.gender == 'Male' else "Ms",
    #     'name': str(customer),
    #     'customer_id': customer.id,
    #     'street': customer.street,
    #     'postcode': customer.postcode,
    #     'place': customer.place,
    #     'last_name': customer.surname,
    #     'creation_date': datetime.today(),
    # }

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, rendered=rendered, by=request.user)
    return HttpResponse(pdf, content_type="application/pdf")
