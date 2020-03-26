from django.views.generic import TemplateView, ListView, CreateView
from mainapp.forms.login import LoginForm
from mainapp.forms.add_manager import AddManagerForm, ManagerForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from mainapp.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout, authenticate


class CreateManagerView(CreateView):
    template_name = 'add_manager.html'
    form_class = ManagerForm
    model = User

    def get_context_data(self, **kwargs):
        context = super(CreateManagerView, self).get_context_data(**kwargs)
        context['operation'] = "Add a"
        return context

    def get_success_url(self):
        return reverse("home", kwargs=dict())


class AddManagerView(TemplateView):
    template_name = 'add_manager.html'

    def get(self, request, *args, **kwargs):
        add_manager_form = AddManagerForm()
        managers_list = User.fetch()

        context = {
            'add_manager_form': add_manager_form,
            'managers': managers_list
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        try:
            add_manager_form = AddManagerForm(request.POST)
            if add_manager_form.is_valid():
                first_name = add_manager_form.cleaned_data.get('first_name')
                surname = add_manager_form.cleaned_data.get('surname')
                phone = add_manager_form.cleaned_data.get('phone')
                username = add_manager_form.cleaned_data.get('username')
                email = add_manager_form.cleaned_data.get('email')
                password = add_manager_form.cleaned_data.get('password')

                manager = User.objects.create_user(email=email, phone=phone, first_name=first_name, surname=surname,
                                                   username=username, password=password)
                if manager:
                    return JsonResponse({
                        'success': True
                    })
                return JsonResponse({
                    'success': False,
                    'message': 'Error in creating Manager'
                })
            elif add_manager_form.errors['email'][0] == 'Already taken':
                return JsonResponse({
                    'success': False,
                    'message': 'Email ' + add_manager_form.errors['email'][0]
                })
            elif add_manager_form.errors['username'][0] == 'Already taken':
                return JsonResponse({
                    'success': False,
                    'message': 'Username' + add_manager_form.errors['username'][0]
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Please Fill All the Fields'
                })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Something Went Wrong. Please Try Again!'
            })


def delete_manager(request, manager_id):
    try:
        user = request.user
        manager = User.fetch(user_id=manager_id)
        if manager:
            manager.delete()
        return redirect('mainapp:add_manager')

    except:
        return redirect('mainapp:add_manager')

