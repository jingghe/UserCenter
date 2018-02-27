#-*- coding: utf-8 -*-
import logging
import ldap
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from Logs.views import messages
from UsersControl import forms
from UsersControl.LDAP.executing_ldap import ExecutingLdap
from UsersControl.accredit.grant import Permissions as _p
from UsersControl.common.formatting import logging_sources
from UsersControl.common.paging import paginators
from UsersControl.models import UserProfile
from UsersControl.templatetags.custom_tag import to_user_permission
from UsersControl.common.CustomViewPermissions import PermissionVerify

logger = logging.getLogger('django_log_file')



@login_required
def user_list(request):
    """获取用户列表"""
    form = forms.AddUserForm
    user_list = UserProfile.objects.all()

    # 分页功能
    page_list = paginators(request, user_list, 20)
    kwvars ={
        'form': form,
        'page_list': page_list,
        'username': request.user,
        'userid': request.user.id,
    }
    if request.user.is_superuser:
        return render(request, 'user/userlist.html',kwvars)
    else:
        return HttpResponseRedirect('/user/change_pwd')


@PermissionVerify()
@login_required
def user_add(request):
    """添加用户"""
    form = forms.AddUserForm
    kwvars = {
        'form': form,
        'request': request,
        'username': request.user,
        'postUrl': '/user/add/',
    }
    if request.method == 'POST':
        form = forms.AddUserForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            login_ip, user = logging_sources(request)
            LDAP_UID = UserProfile.objects.aggregate(Max('uid'))['uid__max']+1 if UserProfile.objects.aggregate(Max(
                'uid'))['uid__max'] else 50000
            password = UserProfile.objects.make_random_password(length=10,
            allowed_chars='abcdefghjklmnpqrstuvwxy~!@#$%\^&*()[\]{}\\|;:,<.>/?\'"\-ABCDEFGHJKLMNPQRSTUVWXY3456789')
            executing_ldap = ExecutingLdap()
            executing_add_user = executing_ldap.executing_add_user_to_LDAP(form, LDAP_UID, password) #创建LDAP账户
            if executing_add_user:
                form.save()
                user_obj = UserProfile.objects.get(username=form.cleaned_data['username'])
                user_obj.uid = LDAP_UID
                user_obj.save()
                messages(user, '创建用户', login_ip, '创建用户%s成功' % nickname)
                _p().push_permissions(form) #推送权限
                return HttpResponseRedirect('/user/list/')
            return HttpResponse('添加用户失败')

    return render(request, 'user/useradd.html', kwvars)


@PermissionVerify()
@login_required
def user_edit(request, ID):
    """修改用户信息"""
    user = get_object_or_404(UserProfile, pk=ID)
    form = forms.EditUserForm(instance=user)
    if request.method == 'POST':
        form = forms.EditUserForm(request.POST, instance=user)
        if form.is_valid():
            if user.username != 'admin':
                if comparison_info(user, form):
                    nickname = form.cleaned_data['nickname']
                    login_ip, user = logging_sources(request)
                    form.save()
                    messages(user, '修改用户', login_ip, '修改用户%s成功' % nickname)
                    _p().push_permissions(form)  # 更新用户信息
            else:
                form.save()
            return HttpResponseRedirect('/user/list/')
    kwvars = {
        'form': form,
        'object': user,
        'request': request,
        'username': request.user,
        'postUrl': '/user/edit/%s/' % ID,
    }
    return render(request, 'user/useredit.html', kwvars)


@PermissionVerify()
@login_required
def user_delete(request,ID):
    """删除用户"""
    user_obj = get_object_or_404(UserProfile, pk=ID)
    if user_obj.username != 'admin':
        executingldap = ExecutingLdap()
        status, res = executingldap.delete_ldap_user(user_obj) #删除LDAP账户
        if status:
            _p().revoke_permissions(user_obj) #回收权限
            UserProfile.objects.filter(id=ID).delete() #删除数据库数据
            login_ip, user = logging_sources(request)
            messages(user, '删除用户', login_ip, '删除用户%s成功' % user_obj.nickname)
            return HttpResponseRedirect('/user/list')
        else:
            HttpResponse(u'删除LDAP账户失败;%s') % res
    return HttpResponse(u'超级管理员不允许删除!!!')


@login_required
def change_pwd(request):
    """修改密码"""
    form = forms.ChangePasswordForm(user=request.user)
    if request.method == 'POST':
        form = forms.ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            if request.user.username != 'admin':
                newpassword = str(form.cleaned_data['new_password2'])
                attr_list = [(ldap.MOD_REPLACE, 'userPassword', str(newpassword)),]
                executing_ldap = ExecutingLdap()
                if executing_ldap.modify_user_to_ldap(request.user, attr_list):
                    form.save()
            else:
                form.save()
            return HttpResponse('密码修改成功')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    _permission = to_user_permission(request.user.id)
    kwvars = {'form': form,
              'username': request.user,
              'permission': _permission,
              'ip': ip}

    return render(request, "user/changepwd.html", kwvars)


@PermissionVerify()
@login_required
def reset_pwd(request, ID):
    """重置用户密码"""
    user_obj = get_object_or_404(UserProfile, pk=ID)
    if user_obj.username != 'admin':
        user = get_object_or_404(UserProfile, pk=ID)
        newpassword = UserProfile.objects.make_random_password(length=10,
        allowed_chars='abcdefghjklmnpqrstuvwxy~!@#$%\^&*()[\]{}\\|;:,<.>/?\'"\-ABCDEFGHJKLMNPQRSTUVWXY3456789')
        attr_list = [(ldap.MOD_REPLACE, 'userPassword', str(newpassword)),]
        executing_ldap = ExecutingLdap()
        if executing_ldap.modify_user_to_ldap(user, attr_list):

            kwvars = {
                'object': user,
                'newpassword': newpassword,
                'username': request.user,
                'request': request,
            }
            return render(request,'user/resetpwd.html', kwvars)
    return HttpResponse('不能重置admin密码')


def comparison_info(user,form):
    """修改用户的LDAP信息"""
    attr_list = [(ldap.MOD_REPLACE, 'givenName', str(form.cleaned_data['nickname'])),
                 (ldap.MOD_REPLACE, 'mail', str(form.cleaned_data['email'])),
                 (ldap.MOD_REPLACE, 'telephoneNumber', str(form.cleaned_data['phone'])),]
    executing_ldap = ExecutingLdap()
    if executing_ldap.modify_user_to_ldap(user, attr_list):
        return True
    return False