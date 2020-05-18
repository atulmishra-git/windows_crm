import xlrd


def import_xls():
    loc_file = 'data_dump.xls'

    wb = xlrd.open_workbook(loc_file)
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
        for col in range(1, len(all_keys)+1):
            d[all_keys[col-1]] = sheet.cell_value(row, col)
        customer_data = {}
        purchase_data = {}

        if not d['email']:
            print('Email missing')
        customer_data['email'] = d['email']
        # check if customer exists

        customer_data['first_name'] = d['first_name']
        customer_data['surname'] = d['surname']
        customer_data['street'] = d['street']
        customer_data['postcode'] = d['postcode']
        customer_data['place'] = d['place']
        customer_data['phone'] = d['phone']

        if d['birthday']:
            customer_data['birthday'] = xlrd.xldate.xldate_as_datetime(d['birthday'], wb.datemode)

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

        purchase_data['kwp'] = d['kwp']
        purchase_data['extra_details'] = d['extra_details']
        purchase_data['project_planning_created'] = d['project_planning_created'] == 'Yes'
        if d['price_with_tax']:
            purchase_data['price_with_tax'] = float(d['price_with_tax'][1:])
        if d['date_sent']:
            purchase_data['date_sent'] = xlrd.xldate.xldate_as_datetime(d['date_sent'], wb.datemode)
        if d['dc_term']:
            purchase_data['dc_term'] = xlrd.xldate.xldate_as_datetime(d['dc_term'], wb.datemode)
        purchase_data['dc_mechanic'] = d['dc_mechanic']
        if d['ac_term']:
            purchase_data['ac_term'] = xlrd.xldate.xldate_as_datetime(d['ac_term'], wb.datemode)
        purchase_data['ac_mechanic'] = d['ac_mechanic']


if __name__ == '__main__':
    import_xls()
