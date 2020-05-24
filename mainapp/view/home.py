from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from mainapp.forms.add_manager import ManagerForm as AddManagerForm
from mainapp.forms.search_user import SearchForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import Customer
from random import randrange


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get(self, request, customer_id=None, *args, **kwargs):
        search_form = SearchForm()
        add_manager_form = AddManagerForm()
        customer = Customer.objects.last()
        if customer:
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': customer,
                'attachments': customer.attachments.order_by('-id')[:5],
            }
        else:
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': dict(),
                'attachments': list(),
            }
        return render(request, self.template_name, context=context)

    def post(self, request):
        query = request.POST.get('name')
        try:
            int_query = int(query)
        except ValueError:
            int_query = 0

        customer_list = {}
        if int_query > 0:
            customer_list = Customer.objects.filter(id=int_query)
        elif query:
            customer_list = Customer.objects.filter(
                Q(first_name__icontains=query) |
                Q(surname__icontains=query) | Q(email__icontains=query) |
                Q(phone__icontains=query) | Q(mobile__icontains=query)
            )

        context = {
            'customers': customer_list
        }
        return render(request, 'home/search_customers.html', context=context)


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
