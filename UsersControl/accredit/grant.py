#-*- coding: utf-8 -*-
import json
from UsersControl.models import Permission, Department, UserProfile
from django.shortcuts import render, render_to_response, get_list_or_404
import requests

class Permissions(object):

    def __init__(self):
        self.push_url_list = None
        self.revoke_url_list = None

    def push_permissions(self, form):
        """
        推送用户信息到用户对应的系统
        :param form: request提交的用户表单数据
        :return:
        """
        data = {'username': form.cleaned_data['username'],
                'tel': form.cleaned_data['tel'],
                'rtx_num': form.cleaned_data['rtx_num'],
                'phone': form.cleaned_data['phone'],
                'department': form.cleaned_data['department'].name,
                'nickname': form.cleaned_data['nickname'],
                'emial': form.cleaned_data['email']}

        push_url_list = self._search_permissions(form, 'push')
        try:
            for i in push_url_list:
                requests.post(i, data=data)
                print push_url_list, json.dumps(data)
        except Exception as e:
            print e

    def revoke_permissions(self, user_obj):
        """
        向用户能够登陆的系统发送回收用户信息消息
        :param form: request提交的用户表单数据
        :return:
        """
        revoke_url_list = self._search_permissions(user_obj, 'revoke')
        for i in revoke_url_list:
            print i

    def _search_permissions(self, form, flag):
        """
        根据添加用户提交的表单获取新用户的权限和所在部门权限
        :param form: request提交的用户表单数据
        :return:返回用户最终权限列表系统的授权API接口，例如：
        set([u'http://cmdb.cmdb.com:28000/api/receive_project_apply_from_oa/', u'http://Apollo.Apollo.com:28000/api/receive_project_apply_from_oa/'])
        """
        if flag == 'push':
            department_permission = [i.create_url for i in Department.objects.get(name=form.cleaned_data['department']).permission.all()]
            user_permission = [Permission.objects.get(name=i).create_url for i in form.cleaned_data['allowable']]
            self.push_url_list = set(department_permission + user_permission)
            return self.push_url_list
        else:
            department_permission = [i.delete_url for i in Department.objects.get(name=UserProfile.objects.get(
                username=form.username).department).permission.all()]
            user_permission = [i.create_url for i in UserProfile.objects.get(username=form.username).allowable.all()]
            self.revoke_url_list = set(department_permission + user_permission)
            return self.revoke_url_list
