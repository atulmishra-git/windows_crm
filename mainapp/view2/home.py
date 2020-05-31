from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView

from mainapp.forms.add_customer import CustomerForm, CustomerAddForm
from mainapp.forms.add_manager import ManagerForm as AddManagerForm
from mainapp.forms.attachments import AttachmentForm
from mainapp.forms.search_user import SearchForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import Customer, PurchaseRecord
from random import randrange


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        search_form = SearchForm()
        add_manager_form = AddManagerForm()
        customer = Customer.objects.last()
        customer_id = request.GET.get('customer', 0)
        try:
            if customer_id:
                customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            pass
        if not customer:
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': dict(),
                'attachments': list(),
                'purchases_last_seven_days': PurchaseRecord.purchases_last_seven_days(),
                'installations_last_six_months': PurchaseRecord.installations_last_six_months()
            }
        else:
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': customer,
                'attachments': customer.attachments.order_by('-id')[:10],
                'purchases_last_seven_days': PurchaseRecord.purchases_last_seven_days(),
                'installations_last_six_months': PurchaseRecord.installations_last_six_months(),
                'all_attachments': customer.attachments.order_by('-id'),
                'attachment_form': AttachmentForm(
                    customer_id=customer.id,
                    request=request
                )
            }
        return render(request, self.template_name, context=context)


class SearchCustomerView(LoginRequiredMixin, TemplateView):
    template_name = 'search/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'customers': Customer.objects.all().order_by('-id'),
            'customer_form': CustomerAddForm()
        }
        return render(request, self.template_name, context=context)


class CustomerHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request, customer_id=None, *args, **kwargs):
        search_form = SearchForm()
        add_manager_form = AddManagerForm()

        customer = {}
        if customer_id:
            customer = Customer.fetch(customer_id=customer_id)
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': customer,
                'attachments': customer.attachments.order_by('-id')[:5]
            }
            return render(request, self.template_name, context=context)

        customer_list = Customer.fetch()
        total_records = None
        if customer_list:
            total_records = customer_list.count()
            random = randrange(total_records)

            customer = customer_list[random]
        context = {
            'search_form': search_form,
            'add_manage_form': add_manager_form,
            'customer': customer
        }
        return render(request, self.template_name, context=context)
