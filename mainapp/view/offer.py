from django.views.generic import TemplateView
from django.shortcuts import render
from mainapp.models import Customer, PurchaseRecord
from django.http import HttpResponse
from django.template.loader import get_template
from mainapp.utils import render_to_pdf


class OfferView(TemplateView):
    template_name = 'offer.html'

    def get(self, request, customer_id, *args, **kwargs):
        purchase_records = PurchaseRecord.fetch(customer_id=customer_id)
        customer = Customer.fetch(customer_id=customer_id)

        context = {
            'customer_id': customer_id,
            'customer': customer,
            'purchases': purchase_records
        }
        return render(request, self.template_name, context=context)


def download_offer(request, purchase_id):
    purchase = PurchaseRecord.fetch_by_id(purchase_id=purchase_id)
    customer = purchase.customer
    fullname = customer.first_name + ' ' + customer.surname
    if customer.gender == 'Male':
        fullname = 'Mr ' + fullname
        gender = 'Mr'
    else:
        gender = 'Ms'
        fullname = 'Ms ' + fullname

    tax = float(purchase.price_without_tax) * 0.19

    p = {
        'gender': gender,
        'name': purchase.customer.first_name + ' ' + purchase.customer.surname,
        'customer_id': customer.id,
        'fullname': fullname,
        'street': customer.street,
        'postcode': customer.postcode,
        'place': customer.place,
        'installation_date': purchase.installation_date.date(),
        'date_month': purchase.installation_date.date(),
        'price_without_tax': purchase.price_without_tax,
        'tax': tax,
        'price_with_tax': purchase.price_with_tax,
        'purchase': purchase
    }

    context = {
        'purchase': p
    }

    # html = template.render(context)
    # pdf = render_to_pdf('pdf/new_offer_310.html', context)
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename = "Invoice_%s.pdf" % "12341231"
    #     content = "inline; filename='%s'" % filename
    #     download = request.GET.get("download")
    #     if download:
    #         content = "attachment; filename='%s'" % filename
    #     response['Content-Disposition'] = content
    #     return response
    # return HttpResponse("Not found")

    return render_to_pdf(
        'pdf/new_offer_310_2.html',
        context
    )
