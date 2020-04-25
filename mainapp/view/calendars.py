import json
from datetime import datetime

from django.db.models import Q
from django.template.response import TemplateResponse

from mainapp.models import PurchaseRecord


def calendar(request, year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month
    purchases = [
        {
            "id": each.id,
            "customer_id": each.customer_id,
            "name": each.customer.first_name + " " + each.customer.surname,
            "dc_term": str(each.dc_term),
            "customer": {
                "purpose": each.customer.purpose,
                "email": each.customer.email,
                "phone": each.customer.phone,
                "offer_id": each.customer.offer_id or "",
                "invoice_id": each.customer.invoice_id or "",
            },
            "purchase": {
                "watt": each.watt,
                "count": each.module_count or "",
                "price": each.price_without_tax or "",
                "offer_date": str(each.offer_date) or "",
                "reseller": each.reseller_name or "",
                "dc_term": str(each.dc_term) or "",
                "dc_mechanic": each.dc_mechanic or "",
                "ac_term": str(each.ac_term) or "",
                "ac_mechanic": each.ac_mechanic or "",
            }
        } for each in PurchaseRecord.objects.filter(
            # Q(
            #     ac_term__month__gte=month - 2,
            #     ac_term__year__gte=year - 1,
            # ) |
            Q(
                dc_term__month__gte=month - 2,
                dc_term__year__gte=year - 1,
            )
        )]
    context = dict(
        objects=json.dumps(purchases)
    )
    return TemplateResponse(request, 'calendars/calendar.html', context)
