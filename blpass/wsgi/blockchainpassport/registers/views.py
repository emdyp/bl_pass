import os
import json
#import reportlab
from xhtml2pdf import pisa
#from django_xhtml2pdf.utils import generate_pdf
#from reportlab.pdfgen import canvas
from django.http import HttpResponse
#from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import render_to_response, get_object_or_404
#from django.core.paginator import Paginator, InvalidPage, EmptyPage
#from django.db.models import Avg, Max, Min
from .models import register


def idview(request, **kwargs):
    """shows html5 render of id"""
    # get arguments
    if 'idNumber' in kwargs:
        idNumber = int(kwargs['idNumber'])
    else:
        idNumber = 1
    # get object
    reg2Show = get_object_or_404(register, pk=idNumber)
    # build response
    dicResponse = json.loads(reg2Show.register_json)
    # render response
    return render_to_response('id.html', dicResponse)


def pdfview(request, **kwargs):
    """shows pdf render of id"""
    # get arguments
    if 'idNumber' in kwargs:
        idNumber = int(kwargs['idNumber'])
    else:
        idNumber = 1
    html = idview(request, idNumber=idNumber)
    current = os.path.dirname(__file__)
    pdfFile = open(os.path.join(current, 'templates', 'test.pdf'), 'w+b')
    pisaStatus = pisa.CreatePDF(html.content, dest=pdfFile) # The errors happens here

    pdfFile.seek(0)
    pdf = pdfFile.read()
    pdfFile.close()
    return HttpResponse(pdf, content_type='application/pdf')


class idListView(ListView):

    model = register

    def get_context_data(self, **kwargs):
        context = super(idListView, self).get_context_data(**kwargs)
        return context