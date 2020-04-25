import json
from datetime import datetime

from django.template.response import TemplateResponse

from mainapp.models import PurchaseRecord


def calendar(request, year=None, month=None):
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    purchases_dc = [
        {
            "id": each.id,
            "customer_id": each.customer_id,
            "name": each.customer.first_name + " " + each.customer.surname,
            "dc_term": str(each.dc_term),
            "customer": {
                "street": each.customer.street or "",
                "postcode": each.customer.postcode or "",
                "place": each.customer.place or ""
            },
            "purchase": {
                # "watt": each.watt,
                # "count": each.module_count or "",
                # "price": each.price_without_tax or "",
                # "offer_date": str(each.offer_date) or "",
                # "reseller": each.reseller_name or "",
                "dc": True,
                "dc_term": str(each.dc_term) or "",
                "dc_mechanic": each.dc_mechanic or "",
            }
        } for each in PurchaseRecord.objects.filter(
            dc_term__month__gte=month-5,
            dc_term__year__gte=year-1,
        )
    ]
    purchases_ac = [
        {
            "id": each.id,
            "customer_id": each.customer_id,
            "name": each.customer.first_name + " " + each.customer.surname,
            "dc_term": str(each.dc_term),
            "customer": {
                "street": each.customer.street or "",
                "postcode": each.customer.postcode or "",
                "place": each.customer.place or ""
            },
            "purchase": {
                "dc": False,
                "ac_term": str(each.ac_term) or "",
                "ac_mechanic": each.ac_mechanic or "",
            }
        } for each in PurchaseRecord.objects.filter(
            ac_term__month__gte=month-5,
            ac_term__year__gte=year-1,
        )
    ]
    context = dict(
        objects=json.dumps(purchases_dc + purchases_ac)
    )
    return TemplateResponse(request, 'calendars/calendar.html', context)
