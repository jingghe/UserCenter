#-*- coding: utf-8 -*-
from UsersControl.common.paging import paginators
from django.shortcuts import render, get_object_or_404
from UsersControl import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from UsersControl.models import Department
from UsersControl.common.formatting import logging_sources
from Logs.views import messages
from UsersControl.common.CustomViewPermissions import PermissionVerify


@PermissionVerify()
@login_required
def department_list(request):
    """获取部门列表"""
    department_obj = Department.objects.all()

    """分页"""
    page_list = paginators(request, department_obj, 20)
    kwvars = {
        'page_list': page_list,
        'request': request,
        'username': request.user,
    }
    return render(request, 'department/departmentlist.html', kwvars)


@PermissionVerify()
@login_required
def department_add(request):
    """增加部门"""
    form = forms.DepartmentAddForm()
    if request.method == 'POST':
        form = forms.DepartmentAddForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            login_ip, user = logging_sources(request)
            form.save()
            messages(user, '创建部门', login_ip, '创建部门%s成功' % name)
            return HttpResponseRedirect('/department/list/')
    kwvars = {
        'form': form,
        'request': request,
        'postUrl': '/department/add/',
        'username': request.user,
    }
    return render(request, 'department/departmentadd.html', kwvars)


@PermissionVerify()
@login_required
def department_edit(request, ID):
    """编辑部门信息"""
    department_obj = get_object_or_404(Department, pk=ID)
    form = forms.DepartmentEditForm(instance=department_obj)
    if request.method == 'POST':
        form = forms.DepartmentEditForm(request.POST, instance=department_obj)
        if form.is_valid():
            name = form.cleaned_data['name']
            login_ip, user = logging_sources(request)
            form.save()
            messages(user, '修改部门', login_ip, '修改部门%s成功' % name)
            return HttpResponseRedirect('/department/list/')

    kwvars = {
        'form': form,
        'object': department_obj,
        'username': request.user,
        'postUrl': '/department/edit/%s/' % ID,
    }
    return render(request, 'department/departmentedit.html', kwvars)


@PermissionVerify()
@login_required
def department_delete(request, ID):
    """删除部门"""
    department_obj = get_object_or_404(Department, pk=ID)
    name = department_obj.name
    login_ip, user = logging_sources(request)
    messages(user, '删除部门', login_ip, '删除部门%s成功' % name)
    department_obj.delete()
    return HttpResponseRedirect('/department/list/')