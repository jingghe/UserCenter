#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HandlesLog(models.Model):
    log_type_choice = ((u'创建用户', u'创建用户'),
                       (u'修改用户', u'修改用户'),
                       (u'删除用户', u'删除用户'),
                       (u'创建权限系统', u'创建权限系统'),
                       (u'修改权限系统', u'修改权限系统'),
                       (u'删除权限系统', u'删除权限系统'),
                       (u'创建部门', u'创建部门'),
                       (u'修改部门', u'修改部门'),
                       (u'删除部门', u'删除部门'),
                       (u'修改密码', u'修改密码'),
                       (u'修改权限', u'修改权限'))
    username = models.CharField(u'用户', max_length=64,)
    date = models.DateTimeField(u'时间', auto_now_add=True)
    log_type = models.CharField(choices=log_type_choice, verbose_name='日志类型', max_length=24)
    source = models.CharField(u'日志来源', max_length=64)
    detail = models.TextField(u'详细日志',)
    component = models.CharField(u'事件子项', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'日志信息'
        verbose_name_plural = u"日志信息"

    def __str__(self):
        return self.source