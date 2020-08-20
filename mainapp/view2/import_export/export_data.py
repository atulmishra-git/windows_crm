from datetime import date

import xlwt
import xlrd
from django.contrib import messages
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import redirect

from mainapp.models import Customer


def export_xls(request):
    customers = Customer.objects.all()

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=data_dump.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Data")

    row_num = 0

    columns = [
        ("Customer Code", 4000),
        ("First Name", 4000),
        ("Family Name", 4000),
        ("Street", 4000),
        ("Postcode", 4000),
        ("Place", 4000),
        ("E - Mail", 4000),
        ("Phone", 4000),
        ("Birthday", 4000),
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
        row = [
            obj.customer_code,
            obj.first_name,
            obj.surname,
            obj.street,
            obj.postcode,
            obj.place,
            obj.email,
            obj.phone,
            obj.birthday
        ]
        for col_num in range(len(row)):
            style = font_style
            val = row[col_num]
            if isinstance(val, date):
                style = date_style
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
        'customer_code',
        'first_name',
        'surname',
        'street',
        'postcode',
        'place',
        'email',
        'phone',
        'birthday',
    ]
    created_customer = 0

    all_keys = customer_keys
    for row in range(1, sheet.nrows):
        d = {}
        for col in range(1, len(all_keys) + 1):
            d[all_keys[col - 1]] = sheet.cell_value(row, col-1)
        customer_data = {}

        if not d['phone']:
            messages.error(request, 'Phone Missing.')
            return redirect('mainapp:new:search')
        customer_data['phone'] = d['phone']

        customer_data['email'] = d['email']
        customer_data['first_name'] = d['first_name']
        customer_data['surname'] = d['surname']
        customer_data['street'] = d['street']
        customer_data['postcode'] = d['postcode']
        customer_data['place'] = d['place']
        customer_data['customer_code'] = d['customer_code']

        # check if customer exists
        customer = Customer(**customer_data)
        if Customer.objects.filter(phone=d['phone']).exists():
            customer = Customer.objects.get(phone=d['phone'])
            for k, v in customer_data.items():
                setattr(customer, k, v)
        else:
            created_customer += 1

        if d['birthday']:
            customer.birthday = xlrd.xldate.xldate_as_datetime(d['birthday'], wb.datemode)
        customer.save()

    messages.success(request, '{} neue kunden'.format(created_customer))
    return redirect('mainapp:new:search')
