#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from Logs.models import HandlesLog
from forms import LogsAddForm
from UsersControl.common.paging import paginators

def logs(request):
    log = HandlesLog.objects.all()

    '''分页'''
    page_list = paginators(request, log, 20)
    kwvars = {
        'request': request,
        'username': request.user,
        'page_list': page_list,
        'postUrl': '/user/add/',
    }
    return render(request, 'logs/logslist.html', kwvars)


def messages(user, log_type, source, detail, component=None):
    kwvars = {
        'username': user,
        'log_type': log_type,
        'source': source,
        'detail': detail,
        'component': component
    }
    form = LogsAddForm(kwvars)
    if form.is_valid():
        form.save()