from django.templatetags.static import register
from django.conf import settings
import os
import base64


@register.filter
def add_ac(obj):
    s1 = obj.dc_purchases.all()
    s2 = obj.ac_purchases.all()
    return int(len(s1)) + int(len(s2))

@register.simple_tag
def pdf_logo():
    logo = os.path.join(settings.BASE_DIR, "cdn", "static", "images", "logo1.png")
    with open(logo, 'rb') as img_file:
        return str(base64.b64encode(img_file.read()), 'utf-8')

@register.filter
def none_to_zero(s):
    return 0 if s is None else s
