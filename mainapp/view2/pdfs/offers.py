from datetime import datetime
import time
import pdfkit
from django.contrib.auth.decorators import login_required

from django.core.files.base import File
from django.http.response import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
import os

from mainapp.models import PurchaseRecord, Customer, Attachments, Pdf

from django.template.response import TemplateResponse

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


def save_to_attachment(customer, kind, rendered, by):
    dt = datetime.now()
    name = f"uploads/{customer.id}-{kind}-" \
           f"{customer.first_name + '-' + customer.surname}-" \
           f"{'%02d' % dt.day}-{'%02d' % dt.month}-{dt.year}.pdf"
    pdfkit.from_string(rendered, os.path.join(settings.BASE_DIR, "media/" + name), options=OPTIONS)
    att = Attachments.objects.create(
        file_name=name.split("/")[-1].split(".")[0],
        kind=kind,
        uploaded_by=by,
        customer_id=customer.id
    )
    att.upload.name = name
    att.save()


@login_required
def download_offer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record
    if purchase.watt == WATT1:
        template_name = 'pdf/offer1_new.html'
    else:
        template_name = 'pdf/offer2_new.html'

    context = {
        'mrms': "Herr" if customer.gender == 'Male' else "Frau",
        'customer': customer,
        'creator': request.user,
        'creation_date': datetime.today(),
    }

    if purchase.watt == WATT1:
        pdf = Pdf.objects.get(name='offer1')
        path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

        with open(path, 'w') as f:
            f.write(pdf.content)
        template_name = "pdf/pdf_"+pdf.name+".html"
    else:
        pdf = Pdf.objects.get(name='offer2')
        path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

        with open(path, 'w') as f:
            f.write(pdf.content)
        template_name = "pdf/pdf_"+pdf.name+".html"

    rendered = render_to_string(template_name,
                                context,
                                request=request)
    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, kind="AB", rendered=rendered, by=request.user)
    os.remove(os.path.join(settings.BASE_DIR, 'mainapp', 'templates', template_name))
    return HttpResponse(pdf, content_type="application/pdf")


def download_offer_confirm(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record

    context = {
        'mrms': "Herr" if customer.gender == 'Male' else "Frau",
        'customer': customer,
        'creator': request.user,
        'creation_date': datetime.today(),
    }

    if purchase.watt == WATT1:
        pdf = Pdf.objects.get(name='offer_confirm1')
        path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

        with open(path, 'w') as f:
            f.write(pdf.content)
        template_name = "pdf/pdf_"+pdf.name+".html"
    else:
        pdf = Pdf.objects.get(name='offer_confirm2')
        path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

        with open(path, 'w') as f:
            f.write(pdf.content)
        template_name = "pdf/pdf_"+pdf.name+".html"

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, kind="AG-B", rendered=rendered, by=request.user)
    os.remove(os.path.join(settings.BASE_DIR, 'mainapp', 'templates', template_name))
    return HttpResponse(pdf, content_type="application/pdf")


def download_install(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record

    pdf = Pdf.objects.get(name='install')
    path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

    with open(path, 'w') as f:
        f.write(pdf.content)
    template_name = "pdf/pdf_"+pdf.name+".html"

    context = {
        'mrms': "Herr" if customer.gender == 'Male' else "Frau",
        'customer': customer,
        'creator': request.user,
        'creation_date': datetime.today(),
    }

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, kind="M-B", rendered=rendered, by=request.user)
    os.remove(os.path.join(settings.BASE_DIR, 'mainapp', 'templates', template_name))
    return HttpResponse(pdf, content_type="application/pdf")


def download_invoice(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    purchase = customer.purchase_record

    pdf = Pdf.objects.get(name='invoice')
    path = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'pdf', "pdf_"+pdf.name+".html")

    with open(path, 'w') as f:
        f.write(pdf.content)
    template_name = "pdf/pdf_"+pdf.name+".html"

    context = {
        'mrms': "Herr" if customer.gender == 'Male' else "Frau",
        'customer': customer,
        'creator': request.user,
        'creation_date': datetime.today(),
        'dc_term_month': getattr(customer.purchase_record.dc_term, 'month', None),
        'dc_term_year': getattr(customer.purchase_record.dc_term, 'year', None)
    }

    rendered = render_to_string(template_name,
                                context,
                                request=request)

    pdf = pdfkit.from_string(rendered, False, options=OPTIONS)
    save_to_attachment(customer=customer, kind="RG", rendered=rendered, by=request.user)
    os.remove(os.path.join(settings.BASE_DIR, 'mainapp', 'templates', template_name))
    return HttpResponse(pdf, content_type="application/pdf")
