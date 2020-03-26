from io import StringIO, BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
import pdfkit
import os
import codecs


# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

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
    html = html.encode('utf-8')
    pdfkit.from_string(html, 'sample.pdf', options=options)

    pdf = open("sample.pdf")
    response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
    response['Content-Disposition'] = 'attachment; filename=sample.pdf'
    pdf.close()
    os.remove("sample.pdf")  # remove the locally created pdf file.
    return response

    # result = BytesIO()
    #
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
