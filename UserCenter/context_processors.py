#_*_coding:utf-8_*_


def template_variable(request):
    user_id = request.user.id
    context = {'userid': user_id}
    request.session.set_expiry(3600)
    return context