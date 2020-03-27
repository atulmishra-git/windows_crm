from django.shortcuts import reverse


class RedirectToHome:
    def get_success_url(self):
        return reverse('mainapp:home', kwargs=dict())
