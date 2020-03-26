from django.views.generic import TemplateView
from mainapp.forms.login import LoginForm
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from mainapp.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout, authenticate


class LoginView(TemplateView):
    template_name = 'login/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mainapp:home')
        login_form = LoginForm()

        context = {
            'login_form': login_form
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = User.fetch(username=username, is_superuser=None)
            if not user:
                return JsonResponse({
                    "success": False,
                    "message": "User not found."

                })
            if authenticate(request, username=username, password=password):
                login(request, user)

                return JsonResponse({
                    'success': True
                })

            else:
                return JsonResponse({
                    "success": False,
                    "message": "Wrong email or password."
                })
        else:
            return JsonResponse({
                "success": False,
                "message": "Please Fill All the Fields."
            })


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    url = reverse('mainapp:login')
    return redirect(url)
