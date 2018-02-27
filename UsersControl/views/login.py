#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django.contrib.auth import login, logout, authenticate
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required #验证用户是否登录
from django.views.decorators.csrf import csrf_exempt #免除验证
from django.views.decorators.debug import sensitive_post_parameters #从错误汇报中滤掉post的敏感信息
from django.views.decorators.csrf import csrf_protect #CSRF保护
from django.views.decorators.cache import never_cache #添加确保响应不被缓存的头部信息
from django.utils.decorators import method_decorator #添加装饰器(普通类视图用的)
# 例如
# @method_decorator(sensitive_post_parameters(), name='dispatch')
# @method_decorator(csrf_protect, name='dispatch')
# @method_decorator(never_cache, name='dispatch')
# def UserLoginView(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect('/add/list/')

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from UsersControl import forms


@sensitive_post_parameters()
@csrf_protect
@never_cache
def user_login(request):
    """用户登录"""
    errors = list()
    form = forms.UserLoginForm(request)
    if request.user.is_authenticated():
        return HttpResponseRedirect('user/list/')
    elif request.method == 'POST':
        form = forms.UserLoginForm(request, data=request.POST)  #使用FORM表单对用户输入进行验证
        if form.is_valid():
            #验证成功后获取用户输入的用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    request.session['user_id'] = user.id
                    # user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    if user.is_superuser:
                        return HttpResponseRedirect(request.POST['next'])
                        return HttpResponseRedirect(request.session['next_path'])
                    else:
                        return HttpResponseRedirect('user/change_pwd')
                else:
                    errors.append(u'用户名或密码过期')
                    return render(request, 'login.html', {'errors': errors})
        else:
            errors.append(u'用户名和密码不正确')
            return render(request, 'login.html', {'errors': errors, 'form': form, 'next': next, })
    return render(request,"login.html", {'form': form, 'next': next, })


def user_logout(request):
    """用户注销"""
    logout(request)  # 销毁Session
    return HttpResponseRedirect('login/')


@csrf_exempt
def page_not_found(request):
    return render_to_response('404.html')


@csrf_exempt
def page_error(request):
    return render_to_response('500.html')

