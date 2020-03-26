from django.views.generic import TemplateView
from mainapp.forms.login import LoginForm
from mainapp.forms.add_customer import AddCustomerForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from mainapp.models import Customer


class AddCustomerView(TemplateView):
    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):
        add_customer_form = AddCustomerForm()

        context = {
            'add_customer_form': add_customer_form
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        try:
            add_customer_form = AddCustomerForm(request.POST)

            if add_customer_form.is_valid():
                first_name = add_customer_form.cleaned_data.get('first_name')
                surname = add_customer_form.cleaned_data.get('surname')
                phone = add_customer_form.cleaned_data.get('phone')
                mobile = add_customer_form.cleaned_data.get('mobile')
                place = add_customer_form.cleaned_data.get('place')
                street = add_customer_form.cleaned_data.get('street')
                postcode = add_customer_form.cleaned_data.get('postcode')
                gender = add_customer_form.cleaned_data.get('gender')
                purpose = add_customer_form.cleaned_data.get('purpose')

                customer = Customer.create(first_name=first_name, surname=surname, phone=phone, place=place,
                                           street=street, postcode=postcode, mobile=mobile)

                if customer:
                    return JsonResponse({
                        'success': True,
                    })

                return JsonResponse({
                    'success': False,
                    'message': 'Error in Adding Customer'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please Fill all the Fields'
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Something Went Wrong. Please Try Again!'
            })
