from datetime import date

import xlwt
import xlrd
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import redirect

from mainapp.models import Customer, PurchaseRecord


def export_xls(request):
    customers = Customer.objects.all()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data_dump.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    row_num = 0

    columns = [
        ("Customer ID", 4000),
        ("First Name", 4000),
        ("Family Name", 4000),
        ("Street", 4000),
        ("Postcode", 4000),
        ("Place", 4000),
        ("E - Mail", 4000),
        ("Phone", 4000),
        ("Birthday", 4000),
        ("", 4000),
        ("Offer - Date", 4000),
        ("Reseller", 4000),
        ("Count of Module", 4000),
        ("Watt", 4000),
        ("Battery + KWH", 4000),
        ("Kwp", 4000),
        ("Additional components", 6000),
        ("Projection created", 4000),
        ("Price", 4000),
        ("Delivery Date", 4000),
        ("DC Date", 4000),
        ("DC Mechanic", 4000),
        ("AC - Date", 4000),
        ("AC Mechanic", 4000),
    ]

    font_style = xlwt.XFStyle()
    ####
    bg_red = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['red']
    bg_red.pattern = pattern

    bg_yellow = xlwt.XFStyle()
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['yellow']
    bg_yellow.pattern = pattern

    ####
    font_style.font.bold = True
    date_style = xlwt.easyxf(num_format_str='DD-MM-YYYY')

    for col_num in range(len(columns)):
        style = bg_yellow
        ws.write(row_num, col_num, columns[col_num][0], style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in customers:
        row_num += 1
        purchase = getattr(obj, "purchase_record", None)
        row = [
            obj.pk,
            obj.first_name,
            obj.surname,
            obj.street,
            obj.postcode,
            obj.place,
            obj.email,
            obj.phone,
            obj.birthday,
            "*****",
        ]
        if purchase is not None:
            row += [
                getattr(purchase, "offer_date", None),
                getattr(purchase, "reseller_name", None),
                getattr(purchase, "module_count", None),
                getattr(purchase, "watt", None),
                "{} {}".format("Yes" if getattr(purchase, "with_battery", None) else "No", getattr(purchase, "kwh", None) or getattr(purchase, "kwh2", None) or ""),
                getattr(purchase, "kwp", None),
                getattr(purchase, "extra_details", None),
                "Yes" if getattr(purchase, "project_planning_created", None) else "No",
                "€{}".format(getattr(purchase, "price_with_tax", None)) if getattr(purchase, "price_with_tax", None) else "",
                getattr(purchase, "date_sent", None),
                getattr(purchase, "dc_term", None),
                getattr(purchase, "dc_mechanic", None),
                getattr(purchase, "ac_term", None),
                getattr(purchase, "ac_mechanic", None),
            ]
        for col_num in range(len(row)):
            style = font_style
            val = row[col_num]
            if isinstance(val, date):
                style = date_style
            elif row[col_num] == "*****":
                style = bg_red
                val = ""
            ws.write(row_num, col_num, val, style)

    wb.save(response)
    return response


def import_xls(request):
    file = request.FILES['xls_file']
    default_storage.save(file.name, file)

    wb = xlrd.open_workbook('media/' + file.name)
    import os
    os.remove('media/' + file.name)
    # take the first sheet
    sheet = wb.sheet_by_index(0)

    customer_keys = [
        'first_name',
        'surname',
        'street',
        'postcode',
        'place',
        'email',
        'phone',
        'birthday',
        '_'
    ]
    purchase_keys = [
        'offer_date',
        'reseller_name',
        'module_count',
        'watt',
        'with_battery',  # if true 'kwh' else 'kwh2'
        'kwp',
        'extra_details',
        'project_planning_created',  # yes/no
        'price_with_tax',  # price with tax
        'date_sent',
        'dc_term',
        'dc_mechanic',
        'ac_term',
        'ac_mechanic',
    ]

    all_keys = customer_keys + purchase_keys
    for row in range(1, sheet.nrows):
        d = {}
        for col in range(1, len(all_keys) + 1):
            d[all_keys[col - 1]] = sheet.cell_value(row, col)
        customer_data = {}
        purchase_data = {}

        if not d['phone']:
            messages.error(request, 'Phone Missing.')
            return redirect('mainapp:list_customer')
        customer_data['phone'] = d['phone']

        customer_data['email'] = d['email']
        customer_data['first_name'] = d['first_name']
        customer_data['surname'] = d['surname']
        customer_data['street'] = d['street']
        customer_data['postcode'] = d['postcode']
        customer_data['place'] = d['place']

        # check if customer exists
        customer = Customer(**customer_data)
        if Customer.objects.filter(phone=d['phone']).exists():
            customer = Customer.objects.get(phone=d['phone'])
            # delete the existing purchase record
            if getattr(customer, 'purchase_record', None):
                customer.purchase_record.delete()
            for k, v in customer_data.items():
                setattr(customer, k, v)

        if d['birthday']:
            customer.birthday = xlrd.xldate.xldate_as_datetime(d['birthday'], wb.datemode)
        customer.save()

        # purchase
        if d['offer_date']:
            purchase_data['offer_date'] = xlrd.xldate.xldate_as_datetime(d['offer_date'], wb.datemode)
        purchase_data['reseller_name'] = d['reseller_name']
        if d['module_count']:
            purchase_data['module_count'] = float(d['module_count'])
        if d['watt']:
            purchase_data['watt'] = float(d['watt'])

        if d['with_battery']:
            with_battery_data, kwh_data = d['with_battery'].split(' ')
            if with_battery_data == 'Yes':
                with_battery = True
                key = 'kwh'
            else:
                with_battery = False
                key = 'kwh2'
            purchase_data['with_battery'] = with_battery
            purchase_data[key] = kwh_data

        # purchase_data['kwp'] = d['kwp']
        purchase_data['extra_details'] = d['extra_details']
        purchase_data['project_planning_created'] = d['project_planning_created'] == 'Yes'
        if d['price_with_tax']:
            purchase_data['price_without_tax'] = float(d['price_with_tax'][1:]) / 1.19
        if d['date_sent']:
            purchase_data['date_sent'] = xlrd.xldate.xldate_as_datetime(d['date_sent'], wb.datemode)
        if d['dc_term']:
            purchase_data['dc_term'] = xlrd.xldate.xldate_as_datetime(d['dc_term'], wb.datemode)
        purchase_data['dc_mechanic'] = d['dc_mechanic']
        if d['ac_term']:
            purchase_data['ac_term'] = xlrd.xldate.xldate_as_datetime(d['ac_term'], wb.datemode)
        purchase_data['ac_mechanic'] = d['ac_mechanic']

        if any([purchase_data.get('module_count'), purchase_data.get('dc_term'), purchase_data.get('ac_term'),
                purchase_data.get('date_sent'), purchase_data.get('watt')]):
            PurchaseRecord.objects.create(customer=customer, **purchase_data)
    return redirect('mainapp:list_customer')
