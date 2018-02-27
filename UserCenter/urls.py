"""UserCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from UsersControl.views import login
from UsersControl.views import user
from UsersControl.views import department
from UsersControl.views import permission
from Logs.views import logs

urlpatterns = [
    url(r'^captcha/?', include('captcha.urls')),
    url(r'^admin/?', admin.site.urls),
    url(r'^logs/?', logs, name='logs'),
    url(r'^login/?$', login.user_login, name='login'),
    url(r'^loout/?$', login.user_logout, name='logout'),
    url(r'^user/add/?$', user.user_add, name='user_add'),
    url(r'^user/list/?$', user.user_list, name='user_list'),
    url(r'^user/edit/(?P<ID>\d+)/?$', user.user_edit, name='user_edit'),
    url(r'^user/delete/(?P<ID>\d+)/?$', user.user_delete, name='user_delete'),
    url(r'^user/reset/password/(?P<ID>\d+)/?$', user.reset_pwd, name='reset_pwd'),

    url(r'^department/list/?$', department.department_list, name='department_list'),
    url(r'^department/add/?$', department.department_add, name='department_add'),
    url(r'^department/edit/(?P<ID>\d+)/?$', department.department_edit, name='department_edit'),
    url(r'^department/delete/(?P<ID>\d+)/?$', department.department_delete, name='department_delete'),

    url(r'^permission/list/?$', permission.permission_list, name='permission_list'),
    url(r'^permission/add/?$', permission.permission_add, name='permission_add'),
    url(r'^permission/edit/(?P<ID>\d+)/?$', permission.permission_edit, name='permission_edit'),
    url(r'^permission/delete/(?P<ID>\d+)/?$', permission.permission_delete, name='permission_delete'),
    url(r'^/?$', user.user_list, name='user_list'),

    url(r'^user/change_pwd?$', user.change_pwd, name='change_pwd'),

]
