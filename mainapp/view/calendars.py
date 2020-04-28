import json
import re
from datetime import datetime, timedelta

from django.template.response import TemplateResponse

from mainapp.models import PurchaseRecord, Tasks


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
    tasks = [
        {
            "id": each.id,
            "creator": str(each.creator),
            "date": str(each.todo_date),
            "time": str(each.todo_time),
            "message": re.sub('\s+', ' ', each.message),
            "user": str(each.user),
            "private": each.private
        }
        for each in Tasks.objects.filter(
            todo_date__gte=now-timedelta(days=90),
            completed=False
        ) if not each.private or (each.private and each.user == request.user)
        # if not private or if private, should be created by self
    ]
    private_tasks = [
        {
            "id": each.id,
            "creator": str(each.creator),
            "date": str(each.todo_date),
            "time": str(each.todo_time),
            "message": re.sub('\s+', ' ', each.message),
            "user": str(each.user)
        }
        for each in Tasks.objects.filter(
            todo_date__gte=now-timedelta(days=90),
            private=True,
            completed=False
        ) if each.user == request.user
    ]
    context = dict(
        purchases=json.dumps(purchases_dc + purchases_ac),
        tasks=json.dumps(tasks),
        private_tasks=json.dumps(private_tasks)
    )
    return TemplateResponse(request, 'calendars/calendar.html', context)
