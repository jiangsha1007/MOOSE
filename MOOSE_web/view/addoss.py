from django.shortcuts import render,redirect
from django.http import HttpResponse
from model.user import *
from model.oss import *
from model.community import *
from view.common import *


def searchoss(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    if request.method == "POST":
        key = request.POST.get('serachoss')
        oss_id = OsslibTopic.objects.filter(topic=key)

        oss_info_all = []
        for per_oss_id in oss_id:
            oss_info = OsslibMeta.objects.filter(community_id=per_oss_id.oss_id)
            if oss_info:
                oss_info_all.append(oss_info[0])
        extra_info.__setitem__('oss', oss_info_all)
        
        return render(request, 'addoss.html', extra_info)
    return render(request, 'addoss.html', extra_info)

