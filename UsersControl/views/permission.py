#-*- coding: utf-8 -*-
from UsersControl.common.paging import paginators
from django.shortcuts import render, render_to_response, get_object_or_404
from UsersControl import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from UsersControl.models import Permission
from UsersControl.common.formatting import logging_sources
from Logs.views import messages
from UsersControl.common.CustomViewPermissions import PermissionVerify


@PermissionVerify()
@login_required
def permission_list(request):
    """获取权限系统列表"""
    per_obj = Permission.objects.all()

    """分页"""
    page_list = paginators(request, per_obj, 20)
    kwvars = {
        'page_list': page_list,
        'request': request,
        'username': request.user,
    }
    return render(request, 'permission/permissionlist.html', kwvars)


@PermissionVerify()
@login_required
def permission_add(request):
    """增加权限系统"""
    form = forms.AddPermissionForm()
    if request.method == 'POST':
        form = forms.AddPermissionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            login_ip, user = logging_sources(request)
            form.save()
            messages(user, '创建权限系统', login_ip, '创建权限系统%s成功' % name)
            return HttpResponseRedirect('/permission/list')
    kwvars = {
        'form': form,
        'request': request,
        'postUrl': '/permission/add/',
        'username': request.user,
    }

    return render(request, 'permission/permissionadd.html', kwvars, )


@PermissionVerify()
@login_required
def permission_edit(request, ID):
    """编辑权限系统信息"""
    permission = get_object_or_404(Permission, pk=ID)
    form = forms.PermissionEditForm(instance=permission)
    if request.method == 'POST':
        form = forms.PermissionEditForm(request.POST, instance=permission)
        if form.is_valid():
            name = form.cleaned_data['name']
            login_ip, user = logging_sources(request)
            form.save()
            messages(user, '修改权限系统', login_ip, '修改权限系统%s成功' % name)
            return HttpResponseRedirect('/permission/list')
    kwvars = {
        'form': form,
        'object': permission,
        'username': request.user,
        'postUrl': '/permission/edit/%s/' % ID,
    }
    return render(request, 'permission/permissionedit.html', kwvars)


@PermissionVerify()
@login_required
def permission_delete(request, ID):
    """删除权限系统"""
    user_obj = get_object_or_404(Permission, pk=ID)
    name = user_obj.name
    login_ip, user = logging_sources(request)
    messages(user, '删除权限系统', login_ip, '删除权限系统%s成功' % name)
    user_obj.delete()
    return HttpResponseRedirect('/permission/list/')