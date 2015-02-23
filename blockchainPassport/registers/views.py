import json
#from django.shortcuts import render
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
        idNumber = 0
    # get object
    reg2Show = get_object_or_404(register, pk=idNumber)
    # build response
    dicResponse = json.loads(reg2Show.register_json)
    # render response
    return render_to_response('id.html', dicResponse)