#-*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginators(request,list_obj,limit):

    '''分页模块,用法:
            1.view中引入：
            ex:from website.common.CommonPaginator import paginators

            2.paginators需要传入三个参数
                (1).request:获取请求数据
                (2).list_obj:为需要分页的数据（一般为*.objects.all()取出来数据）
                (3).limit:为每页显示的条数
            ex:lst = paginators(request,mList, 5)

            3.view需要获取paginators return的lst，并把lst返回给前端模板
            ex:kwvars = {'lPage':lst,}

            4.前端需要for循环lPage也就是lst读取每页内容
            ex:{% for i in lPage %} ... {% endfor %}

            5.模板页引入paginator.html
            ex:{% include "common/paginator.html" %}
        '''
    paginator = Paginator(list_obj, int(limit))
    page = request.GET.get('page')
    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    return page_list