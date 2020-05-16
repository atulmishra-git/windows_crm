from django.http.response import JsonResponse
from django.views.generic import TemplateView
from mainapp.forms.login import LoginForm
from django.shortcuts import render, redirect, reverse
from mainapp.models import User
from django.contrib.auth import login, logout


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
        if not login_form.is_valid():
            context = {
                'login_form': login_form
            }

            return render(request, self.template_name, context=context)

        user = User.objects.get(username__iexact=login_form.cleaned_data['username'])
        login(request, user)
        return redirect('mainapp:home')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    url = reverse('mainapp:login')
    return redirect(url)


def heartbeat(request):
    return JsonResponse(data={}, status=200)
