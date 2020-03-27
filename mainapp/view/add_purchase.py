from django.views.generic import TemplateView
from mainapp.forms.add_purchase_record import AddPurchaseRecordForm
from mainapp.forms.add_customer import CustomerForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from mainapp.models import PurchaseRecord


class AddPurchaseView(TemplateView):
    template_name = 'add_purchase.html'

    def get(self, request, *args, **kwargs):
        add_purchase_record = AddPurchaseRecordForm()

        context = {
            'add_purchase': add_purchase_record
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        try:
            add_purchase_record = AddPurchaseRecordForm(request.POST)

            if add_purchase_record.is_valid():
                customer = add_purchase_record.cleaned_data.get('customer')
                reseller_name = add_purchase_record.cleaned_data.get('reseller_name')
                module_count = add_purchase_record.cleaned_data.get('module_count')
                module_type = add_purchase_record.cleaned_data.get('module_type')
                memory_type = add_purchase_record.cleaned_data.get('memory_type')
                kwp = add_purchase_record.cleaned_data.get('kwp')
                price_without_tax = add_purchase_record.cleaned_data.get('price_without_tax')
                price_with_tax = add_purchase_record.cleaned_data.get('price_with_tax')
                offer_created = add_purchase_record.cleaned_data.get('offer_created')
                cancellation = add_purchase_record.cleaned_data.get('cancellation')
                project_planning_created = add_purchase_record.cleaned_data.get('project_planning_created')
                installation_date = add_purchase_record.cleaned_data.get('installation_date')
                ac_date = add_purchase_record.cleaned_data.get('ac_date')
                photo_roof_access = add_purchase_record.cleaned_data.get('photo_roof_access')
                photo_counter_cabinet = add_purchase_record.cleaned_data.get('photo_counter_cabinet')
                video_counter = add_purchase_record.cleaned_data.get('video_counter')
                photo_of_counter = add_purchase_record.cleaned_data.get('photo_of_counter')
                power_of_attorney = add_purchase_record.cleaned_data.get('power_of_attorney')
                data_collection = add_purchase_record.cleaned_data.get('data_collection')
                order_date = add_purchase_record.cleaned_data.get('order_date')
                with_battery = add_purchase_record.cleaned_data.get('with_battery')

                purchase_record = PurchaseRecord.create(customer_id=customer.id, reseller_name=reseller_name,
                                                        module_count=module_count, module_type=module_type, kwp=kwp,
                                                        price_without_tax=price_without_tax,
                                                        price_with_tax=price_with_tax,
                                                        offer_created=offer_created, cancellation=cancellation,
                                                        project_planning_created=project_planning_created,
                                                        installation_date=installation_date, ac_date=ac_date,
                                                        photo_roof_area=photo_roof_access,
                                                        photo_counter_cabinet=photo_counter_cabinet,
                                                        video_counter=video_counter,
                                                        photo_of_counter=photo_of_counter,
                                                        power_of_attorney=power_of_attorney,
                                                        data_collection=data_collection, order_date=order_date,
                                                        memory_type=memory_type, with_battery=with_battery)

                if purchase_record:
                    return JsonResponse({
                        'success': True
                    })

                return JsonResponse({
                    'success': False,
                    "message": "Error in Creating Purchase Record"
                })
            else:
                return JsonResponse({
                    'success': False,
                    "message": "Please Fill All the Fields"
                })

        except Exception as e:
            print("Exception occurs in creating Purchase Record. Error: {}".format(str(e)))
            return JsonResponse({
                'success': False,
                "message": "Something Went Wrong"
            })
