from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# for translate to fa language
from django.utils.translation import ugettext as _


def verify(request):
    if request.GET.get('status') == 'OK':
        p = Payment.object.get(autority=request.GET['Authority'])
        return p.verify(request)
    else:
        return HttpResponse(_('Transaction failed or canceled by user'))
