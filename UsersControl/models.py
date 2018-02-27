#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ast
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import django.utils.timezone
from django.core.validators import MaxValueValidator, RegexValidator

# Create your models here.

#
# class PermissionList(models.Model):
#     name = models.CharField(max_length=64)
#     url = models.CharField(max_length=255)
#
#     def __unicode__(self):
#         return '%s(%s)' %(self.name,self.url)
#
#
# class RoleList(models.Model):
#     name = models.CharField(max_length=64)
#     permission = models.ManyToManyField(PermissionList,null=True,blank=True)
#     #permission = models.CharField(max_length=256, blank=True, null=True)
#
#     def __unicode__(self):
#         return self.name


class loginuser(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                username=username,
                                password=password,)

        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# class User(AbstractBaseUser):
#     username = models.CharField(max_length=40, unique=True, db_index=True)
#     email = models.EmailField(max_length=255)
#     is_active = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     nickname = models.CharField(max_length=64, null=True)
#     sex = models.CharField(max_length=2, null=True)
#     role = models.ForeignKey(RoleList,null=True,blank=True)
#     phone = models.CharField(max_length=40, unique=True, db_index=True)
#
#     objects = loginuser()
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     def has_perm(self,perm,obj=None):
#         if self.is_active and self.is_superuser:
#             return True


class UserProfile(AbstractBaseUser):
    sex_choice = ((u'女', u'女'), (u'男', u'男'))
    email = models.EmailField(verbose_name='邮箱地址', max_length=255)
    is_active = models.BooleanField(u'是否启用', default=True)
    is_superuser = models.BooleanField(u'是否管理员', default=False)
    username = models.CharField(u'账户', max_length=40, unique=True, db_index=True)
    nickname = models.CharField(u'姓名', max_length=64, null=True)
    token = models.CharField(u'token', max_length=128, default=None, blank=True, null=True)
    allowable = models.ManyToManyField('Permission', verbose_name='允许权限', related_name='allowable_permission',
                                       blank=True)
    prohibited = models.ManyToManyField('Permission', verbose_name='禁止权限', related_name='prohibited_permission',
                                        blank=True)
    department = models.ForeignKey('Department', verbose_name=u'部门', null=True, blank=True)
    sex = models.CharField(u'性别', choices=sex_choice, max_length=2, default=0, null=True)
    tel = models.CharField(u'座机', max_length=32, validators=[RegexValidator(r'^\d{0,9}$')], default=None, blank=True,null=True)
    rtx_num = models.CharField(u'RTX账号', max_length=32, default=None, blank=True, null=True)
    phone = models.CharField(u'手机', max_length=11, validators=[RegexValidator(r'^\d{0,9}$')], default=None, blank=True, null=True)
    uid = models.IntegerField(u'UID', null=True, blank=True)
    memo = models.TextField(u'备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(u'创建时间', blank=True, auto_now_add=True)
    valid_begin_time = models.DateTimeField(u'有效期开始时间', default=django.utils.timezone.now)
    valid_end_time = models.DateTimeField(u'有效期结束时间', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = u"用户信息"

    def __str__(self):
        return self.username

    objects = loginuser()


class Department(models.Model):
    name = models.CharField(u'部门', max_length=64, unique=True)
    permission = models.ManyToManyField('Permission', verbose_name='可登陆系统', blank=True)
    #mome = models.TextField(u'备注', blank=True, null=True, default=None)

    class Meta:
        verbose_name = u'用户部门'
        verbose_name_plural = u"用户部门"

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(verbose_name='系统名称', max_length=64, unique=True)
    user = models.CharField(u'API验证用户', max_length=64, null=True, blank=True)
    token = models.CharField(u'API token', max_length=128, null=True, blank=True)
    create_url = models.CharField(u'用户授权API', max_length=255)
    delete_url = models.CharField(u'用户回收API', max_length=255)

    class Meta:
        verbose_name = u'授权'
        verbose_name_plural = u"授权"

    def __str__(self):
        return self.name
