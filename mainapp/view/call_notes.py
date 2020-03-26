from django.views.generic import TemplateView
from mainapp.forms.call_notes import AddCallNotesForm
from django.shortcuts import render
from mainapp.models import Customer, CallNotes
from django.http import JsonResponse


class CallNotesView(TemplateView):
    template_name = 'call_notes.html'

    def get(self, request, customer_id, *args, **kwargs):
        add_call_notes = AddCallNotesForm()

        customer = Customer.fetch(customer_id=customer_id)
        call_notes = CallNotes.fetch(customer_id=customer)

        context = {
            'add_call_notes': add_call_notes,
            'customer_id': customer_id,
            'customer': customer,
            'call_notes': call_notes

        }
        return render(request, self.template_name, context=context)

    def post(self, request, customer_id):
        try:
            customer_id = request.POST.get('customer_id')
            add_call_notes = AddCallNotesForm(request.POST)
            user_id = request.user.id

            if add_call_notes.is_valid():
                notes = add_call_notes.cleaned_data.get('notes')

                call_notes = CallNotes.create(customer_id=customer_id, user_id=user_id, notes=notes)
                if call_notes:
                    return JsonResponse({
                        'success': True,
                    })

                return JsonResponse({
                    'success': False,
                    'message': "Can't create the call note. Please try again"
                })

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please Fill All the Fields.'
                })

        except Exception as e:
            print("Exception occurs in Creating Call Notes View. Error: {}".format(str(e)))
            return JsonResponse({
                'success': False,
                'message': "Something went wrong. Please Try Again!"
            })
