# _*_coding:utf-8_*_
from django import forms
import sys
from django.contrib import auth
from django.contrib.auth import get_user_model
from UsersControl.models import UserProfile,Department,Permission,Permission
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField
from UsersControl.common.CheckPassword import check_password
import time
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

class UserLoginForm(forms.Form):
    username = forms.CharField(label=u'账 号', error_messages={'required': u'账号不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'密 码', error_messages={'required': u'密码不能为空'},
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    #captcha = CaptchaField()

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(UserLoginForm, self).__init__(*args, **kwargs)


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=u'原始密码', error_messages={'required': '请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label=u'新密码', error_messages={'required': '请输入新密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=u'重复输入', error_messages={'required': '请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = UserProfile.objects.get(username=user.username)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        self.old_password = self.cleaned_data["old_password"]
        user = authenticate(username=self.user.username, password=self.old_password)
        if not user:
            raise forms.ValidationError(u'原密码错误')
        return self.old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1) < 7:
            raise forms.ValidationError(u'密码必须大于7位！')
        if not check_password(password1):
            raise forms.ValidationError(u'密码复杂性不符合要求！')
        if password1 == self.old_password:
            raise forms.ValidationError(u'新密码与旧密码相同！')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(u'两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class AddUserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'nickname', 'email', 'phone', 'tel', 'rtx_num', 'department', 'is_active',
                  'sex', 'allowable', )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'rtx_num': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.RadioSelect(choices=UserProfile.sex_choice, attrs={'class': 'form-control'}),
            'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')), attrs={'class': 'form-control'}),
            'allowable': forms.CheckboxSelectMultiple(choices=Permission.objects.values(),
                                                      attrs={'class': 'form-control'}),
            'department': forms.Select(choices=Department.objects.values(), attrs={'class': 'form-control'})
         }

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = u'账 户'
        self.fields['username'].error_messages = {'required': u'请输入账号'}
        self.fields['email'].label = u'邮 箱'
        self.fields['email'].error_messages = {'required': u'请输入邮箱', 'invalid': u'请输入有效邮箱'}
        self.fields['phone'].label = u'电 话'
        self.fields['phone'].error_messages = {'required': u'请输入电话号码'}
        self.fields['tel'].label = u'座 机'
        self.fields['tel'].error_messages = {'required': u'请输入座机号码'}
        self.fields['rtx_num'].label = u'RTX号码'
        self.fields['rtx_num'].error_messages = {'required': u'请输入RTX号码'}
        self.fields['nickname'].label = u'姓 名'
        self.fields['nickname'].error_messages = {'required': u'请输入姓名'}
        self.fields['sex'].label = u'性 别'
        self.fields['sex'].error_messages = {'required': u'请选择性别'}
        self.fields['is_active'].label = u'状 态'
        self.fields['allowable'].label = u'允许登陆系统'


class EditUserForm(AddUserForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'nickname', 'email', 'phone', 'tel', 'rtx_num', 'department', 'is_active',
                  'sex', 'allowable',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'rtx_num': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.RadioSelect(choices=UserProfile.sex_choice, attrs={'class': 'form-control'}),
            'is_active': forms.Select(choices=((True, u'启用'), (False, u'禁用')), attrs={'class': 'form-control'}),
            'allowable': forms.CheckboxSelectMultiple(choices=Permission.objects.values(),
                                                      attrs={'class': 'form-control'}),
            'department': forms.Select(choices=Department.objects.values(), attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        return self.cleaned_data['password']


class gerenForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('email', 'phone', 'nickname', 'sex')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.RadioSelect(choices=((u'男', u'男'), (u'女', u'女')), attrs={'class': 'list-inline'}),
        }

    def __init__(self, *args, **kwargs):
                super(gerenForm, self).__init__(*args,**kwargs)
                self.fields['email'].label = u'邮 箱'
                self.fields['email'].error_messages={'required': u'请输入邮箱', 'invalid': u'请输入有效邮箱'}
                self.fields['phone'].label = u'电 话'
                self.fields['phone'].error_messages={'required': u'请输入电话号码'}
                self.fields['nickname'].label = u'姓 名'
                self.fields['nickname'].error_messages = {'required': u'请输入姓名'}
                self.fields['sex'].label = u'性 别'
                self.fields['sex'].error_messages = {'required': u'请选择性别'}


class AddPermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name', 'user', 'token', 'create_url', 'delete_url')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'create_url': forms.TextInput(attrs={'class': 'form-control'}),
            'delete_url': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddPermissionForm, self).__init__(*args,**kwargs)
        self.fields['name'].label = u'系统名称'
        self.fields['name'].error_messages = {'required': u'请输入名称'}
        self.fields['create_url'].label = u'用户权限授权API'
        self.fields['create_url'].error_messages={'required': u'请输入授权URL'}
        self.fields['delete_url'].label = u'用户权限回收API'
        self.fields['delete_url'].error_messages = {'required': u'请输入回收URL'}
        self.fields['user'].label = u'API验证用户'
        self.fields['user'].error_messages = {'required': u'请输入API接口认证用户'}
        self.fields['token'].label = u'API验证token'
        self.fields['token'].error_messages = {'required': u'请输入API验证token'}


class PermissionEditForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name', 'user', 'token', 'create_url', 'delete_url')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'create_url': forms.TextInput(attrs={'class': 'form-control'}),
            'delete_url': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'token': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PermissionEditForm, self).__init__(*args, **kwargs)


class DepartmentAddForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'permission')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permission': forms.CheckboxSelectMultiple(choices=Permission.objects.values('id', 'name'),
                                                       attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = u'部门名称'
        self.fields['name'].error_messages = {'required': u'请输入名称'}
        self.fields['permission'].label = u'添加授权'
        self.fields['permission'].error_messages = {'required': u'请输入名称'}


class DepartmentEditForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'permission')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'permission': forms.CheckboxSelectMultiple(choices=Permission.objects.values('id', 'name'),
                                                       attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentEditForm, self).__init__(*args, **kwargs)