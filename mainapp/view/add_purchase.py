from django.views.generic import CreateView
from mainapp.forms.add_purchase_record import PurchaseRecordForm
from mainapp.models import PurchaseRecord


class AddPurchaseView(CreateView):
    template_name = 'add_purchase.html'
    form_class = PurchaseRecordForm
    model = PurchaseRecord
