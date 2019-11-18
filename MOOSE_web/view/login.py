from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from model.user import *
from view.common import *


def index(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect("/login/")
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    return render(request, 'index.html', extra_info)


def login(request):
    if request.session.get('is_login', None) and request.session['is_login'] is True:
        return redirect('/index/')
    if request.method == "POST":
        username = request.POST.get('loginUsername')
        password = request.POST.get('loginPassword')
        try:
            user = OsslibAdmin.objects.get(user_name=username)
        except BaseException as ex:
            print(ex)
            return render(request, 'login/login.html')
        if user.user_pasword == password:
            try:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
            except BaseException as ex:
                print(ex)
            #
            #
            return redirect('/index/')
    return render(request, 'login/login.html', locals())


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return HttpResponseRedirect("/index/")
    request.session.flush()  # 或者使用下面的方法
    return redirect('/index/')