import xlwt
from datetime import date
from django.http import HttpResponse

from mainapp.models import Customer


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
    pass
