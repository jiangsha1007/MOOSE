from django.shortcuts import render,redirect
from django.http import HttpResponse
from model.oss import *
from model.community import *
from model.platform import *
from view.common import *
from view.request_header import *
import time
import base64


def new(request):
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    oss_meta_list = MOOSEMeta.objects.filter(uid=uid, status=1)
    oss_mata = dict()
    oss_mata.__setitem__('oss_list', oss_meta_list)
    oss_mata.__setitem__('oss_list_count', len(oss_meta_list))
    extra_info.update(oss_mata)
    return render(request, 'new.html', extra_info)


def addtolist(request):
    uid = request.session['user_id']
    repo_name = request.POST.get('repo_name')
    platform_id = request.POST.get('platform_id')
    oss_platform_api = MOOSEPlatform.objects.get(id=platform_id)
    if oss_platform_api:
        get_single_api = oss_platform_api.get_oss_single_api
    repo_url = get_single_api + repo_name
    try:
        repo_data = get_html_json(repo_url, getHeader())[0]
    except:
        pass
    oss_meta_item = MOOSEMeta()
    oss_meta_item.oss_fullname = repo_data['full_name']
    oss_meta_item.oss_name = repo_data['name']
    oss_meta_item.oss_id = repo_data['id']
    oss_meta_item.oss_description = repo_data['description']
    try:
        oss_meta_item.oss_create_time = repo_data['created_at']
    except BaseException as e:
        oss_meta_item.oss_create_time = ''
    try:
        oss_meta_item.oss_owner_id = int(repo_data['owner']['id'])
    except BaseException as ex:
        oss_meta_item.oss_owner_id = 0
    try:
        oss_meta_item.oss_owner_type = repo_data['owner']['type']
    except BaseException as ex:
        oss_meta_item.oss_owner_type = ''
    try:
        oss_meta_item.oss_size = int(repo_data['size'])
    except BaseException as ex:
        oss_meta_item.oss_size = 0
    try:
        oss_meta_item.oss_star = repo_data['stargazers_count']
    except BaseException as ex:
        oss_meta_item.oss_star = 0
    try:
        oss_meta_item.oss_fork = repo_data['forks']
    except BaseException as ex:
        oss_meta_item.oss_fork = 0

    try:
        oss_meta_item.oss_main_language = repo_data['language']
    except BaseException as ex:
        oss_meta_item.oss_main_language = ''
    try:
        oss_meta_item.oss_homepage = repo_data['homepage']
    except BaseException as e:
        oss_meta_item.oss_homepage = ''
    try:
        oss_meta_item.oss_license = repo_data['license']['name']
    except BaseException as e:
        oss_meta_item.oss_license = ''
    try:
        oss_meta_item.oss_git_url = repo_data['clone_url']
        oss_meta_item.oss_git_tool = 'Git'
    except BaseException as e:
        oss_meta_item.oss_git_url = ''
        oss_meta_item.oss_git_tool = ''
    try:
        oss_meta_item.has_wiki = int(repo_data['has_wiki'])
    except BaseException as ex:
        oss_meta_item.has_wiki = 0
    oss_meta_item.last_update_date = repo_data['updated_at']
    oss_meta_item.update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    readmeinfo = get_html_json(repo_data['url'] + "/readme", getHeader())[0]
    if len(readmeinfo) > 0:
        try:
            readme = readmeinfo['content']
            oss_meta_item.readme = str(base64.b64decode(readme), encoding="utf-8").replace('\r', '').replace('\n','')
        except:
            oss_meta_item.readme = ''
    oss_meta_item.uid = uid
    oss_meta_item.status = 1
    oss_meta_item.save()
    return HttpResponse(repo_data, content_type='application/text')

def addtomonitor(request):
    uid = request.session['user_id']
    monitor_name = request.POST.get('monitor_name')
    oss_community = MOOSECommunity()
    oss_community.user_id = uid
    oss_community.community_name = monitor_name
    oss_community.status = 0
    oss_community.save()
    oss_meta_list = MOOSEMeta.objects.filter(uid=uid, status=1)
    if oss_meta_list:
        for per_oss_meta in oss_meta_list:
            oss_community_list = MOOSECommunityList()
            oss_community_list.community_id = oss_community.id
            oss_community_list.oss_name = per_oss_meta.oss_fullname
            oss_community_list.oss_id = per_oss_meta.oss_id
            oss_community_list.meta_id = per_oss_meta.id
            oss_community_list.save()
            oss_meta_list.update(status=2)
    return HttpResponse('1', content_type='application/text')