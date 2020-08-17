from django.templatetags.static import register


@register.filter
def get(value, arg):
    return value.get(arg)

@register.filter
def add(obj):
    s1 = obj.dc_purchases.all()
    s2 = obj.ac_purchases.all()
    return int(len(s1)) + int(len(s2))
