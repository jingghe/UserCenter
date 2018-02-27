#-*- coding: utf-8 -*-

def logging_sources(request):
    login_ip = request.META.get('REMOTE_ADDR', '')
    user = request.user
    return login_ip, user