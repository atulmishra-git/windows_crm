from django.templatetags.static import register


@register.filter
def get(value, arg):
    return value.get(arg)

@register.filter
def add(s1, s2):
    return int(len(s1)) + int(len(s2))
