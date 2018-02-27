#-*- coding: utf-8 -*-


from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect, render_to_response,render
from UsersControl.models import UserProfile


def PermissionVerify():
    '''权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    '''
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iUser = UserProfile.objects.get(username=request.user)
            if not iUser.is_superuser: #判断用户如果是超级管理员则具有所有权限
                return HttpResponseRedirect('/user/change_pwd')
            else:
                pass
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator
