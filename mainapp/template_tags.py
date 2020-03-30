from django.templatetags.static import register


@register.filter
def get(value, arg):
    return value.get(arg)
