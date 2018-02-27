#-*- coding: utf-8 -*-

import re
from UsersControl.models import Permission, Department,UserProfile
from django import template
register = template.Library()


@register.filter
def to_department_permission(id):
    """获取部门可登陆系统权限"""
    try:
        department_obj = Department.objects.filter(id=id)
        if department_obj:
            department_obj = department_obj[0]
            permission_list = [i.name for i in department_obj.permission.all()]
            permission_list = ",".join(permission_list)
            return permission_list
    except Exception as e:
        return '获取部门权限错误'


@register.filter
def to_user_permission(id):
    """获取用户可登陆权限"""
    try:
        user_obj = UserProfile.objects.filter(id=id)[0]
        user_permission_list = [i.name for i in user_obj.allowable.all()]
        department_obj = Department.objects.filter(id=user_obj.department_id)
        if department_obj:
            department_obj = department_obj[0]
            department_permission_list = [i.name for i in department_obj.permission.all()]
            permission_list = set(department_permission_list + user_permission_list)
        else:
            permission_list = user_permission_list
        permission_list = ", ".join(permission_list)
        return permission_list
    except Exception as e:
        print e
        return '获取用户权限错误'
