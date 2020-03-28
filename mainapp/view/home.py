from django.views.generic import TemplateView
from mainapp.forms.add_manager import ManagerForm as AddManagerForm
from mainapp.forms.search_user import SearchForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import Customer
from random import randrange
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, customer_id=None, *args, **kwargs):
        search_form = SearchForm()
        add_manager_form = AddManagerForm()
        customers = Customer.objects.values('id', 'first_name', 'email')

        customer_dict = {}
        if customer_id:
            customer_dict = Customer.fetch(customer_id=customer_id)
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': customer_dict,
                'customers': customers
            }
            return render(request, self.template_name, context=context)

        customer_list = Customer.fetch()
        total_records = None
        if customer_list:
            total_records = customer_list.count()
            random = randrange(total_records)

            customer_dict = customer_list[random]
        context = {
            'search_form': search_form,
            'add_manage_form': add_manager_form,
            'customer': customer_dict
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        customer_name = request.POST.get('name')

        customer_list = {}
        if customer_name:
            customer_list = Customer.fetch(name=customer_name)

        context = {
            'customers': customer_list
        }
        return render(request, 'home/search_customers.html', context=context)


class CustomerHomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request, customer_id=None, *args, **kwargs):
        search_form = SearchForm()
        add_manager_form = AddManagerForm()

        customer_dict = {}
        if customer_id:
            customer_dict = Customer.fetch(customer_id=customer_id)
            context = {
                'search_form': search_form,
                'add_manage_form': add_manager_form,
                'customer': customer_dict
            }
            return render(request, self.template_name, context=context)

        customer_list = Customer.fetch()
        total_records = None
        if customer_list:
            total_records = customer_list.count()
            random = randrange(total_records)

            customer_dict = customer_list[random]
        context = {
            'search_form': search_form,
            'add_manage_form': add_manager_form,
            'customer': customer_dict
        }
        return render(request, self.template_name, context=context)
