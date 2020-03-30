from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import pdfkit
import os


def render_to_pdf(template_src, context):
    template = get_template(template_src)
    # context = Context(context_dict)
    html = template.render(context)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(html,)
