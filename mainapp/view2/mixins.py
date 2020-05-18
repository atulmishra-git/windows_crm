from django.shortcuts import reverse


class RedirectToHome:
    def get_success_url(self):
        return reverse('mainapp:home', kwargs=dict())


class FilterListMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter_form'] = self.filter.form
        return context
