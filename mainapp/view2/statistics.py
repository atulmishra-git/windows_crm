from django.shortcuts import render
from mainapp.models import Customer
from django.http import JsonResponse
from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Reseller
from django.db.models.aggregates import Sum, Count
from django.db.models.functions import Extract


def months():
    lst = [_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'),
    _('October'), _('November'), _('December')]
    results = []
    for i in range(0, len(lst)):
        results.append((i+1, lst[i]))
    return results


def years():
    results = []
    for i in range(2010, 2090):
        x = str(i)
        results.append((i, x))
    return results


class StatsForm(forms.Form):
    reseller = forms.ModelChoiceField(label=_('Reseller'), queryset=Reseller.objects.all())
    view_type = forms.ChoiceField(label=_('View Type'), widget=forms.Select, choices=[(1, _('Monthly')), (2, _('Yearly'))])
    month = forms.ChoiceField(label=_('Month'), widget=forms.Select, choices=months())
    year = forms.ChoiceField(label=_('Year'), widget=forms.Select, choices=years())


def index(request):
    context = {}
    context['customer'] = Customer.objects.last()
    context['form'] = StatsForm()
    return render(request, "statistics/index.html", context)


def render_chart(request):
    labels = []
    data = []
    totals = {}
    if request.method == 'POST':
        reseller = Reseller.objects.get(pk=int(request.POST['reseller']))
        month = request.POST.get('month')
        year = request.POST.get('year')
        view_type = request.POST.get('view_type')
        lst = ['Janaury', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        if int(view_type) == 1 and month:
            label = lst[int(month)-1]
            queryset = Reseller.objects.filter(pk=int(request.POST['reseller'])).\
            annotate(month=Extract('purchases__date_of_receipt', 'month')).\
            values('purchases__date_of_receipt').\
            filter(month=month).order_by('purchases__date_of_receipt').annotate(count=Count('month'))

            totals['month'] = 0
            for entry in queryset:
                data.append(entry['count'])
                labels.append(entry['purchases__date_of_receipt'])
                totals['month'] += entry['count']

        if int(view_type) == 2 and year:
            label = year
            label = lst[int(month)-1]
            queryset = Reseller.objects.filter(pk=int(request.POST['reseller'])).\
            annotate(year=Extract('purchases__date_of_receipt', 'year'), month=Extract('purchases__date_of_receipt', 'month')).\
            values('month').\
            filter(year=year).order_by('year').annotate(count=Count('year'))

            totals['year'] = 0
            for entry in queryset:
                data.append(entry['count'])
                labels.append(lst[int(entry['month'])-1])
                totals['year'] += entry['count']

    return JsonResponse(
        data={
            'labels': labels,
            'data': data,
            'totals': totals
        }
    )
