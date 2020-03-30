from datetime import datetime

import pdfkit
from django.http.response import HttpResponse
from django.template.loader import render_to_string

from mainapp.models import PurchaseRecord


def download_offer(request, purchase_id):
    purchase = PurchaseRecord.objects.last()
    customer = purchase.customer

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

    rendered = render_to_string('pdf/offer1.html',
                                context,
                                request=request)
    options = {
        'page-size': 'A4',
        'margin-top': '0.7842in',
        'margin-right': '0.9842in',
        'margin-bottom': '0.7842in',
        'margin-left': '0.9842in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdf = pdfkit.from_string(rendered, False, options=options)
    return HttpResponse(pdf, content_type="application/pdf")
