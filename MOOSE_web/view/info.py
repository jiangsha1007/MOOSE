from django.shortcuts import render,redirect
from django.http import HttpResponse
from model.community import *
from model.oss import *
from view.common import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum, Count
from operator import itemgetter

def commit(request):
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    cid = request.GET.get('cid')
    commit_yearmonth = OsslibStatisticCommitYearmonth.objects.filter(community_id=int(cid))
    line_commit_arr = ''
    line_commit_data = ''
    line_issue_close_data = ''
    if commit_yearmonth.count() > 0:
        for per_commit_yearmonth in commit_yearmonth:
            line_commit_data += str(per_commit_yearmonth.commits_count) + ','
            line_commit_arr += per_commit_yearmonth.yearmonth + ','

    issue_yearmonth = OsslibStatisticIssueYearmonth.objects.filter(community_id=int(cid))
    line_issue_arr = ''
    line_issue_data = ''
    if issue_yearmonth.count() > 0:
        for per_issue_yearmonth in issue_yearmonth:
            line_issue_data += str(per_issue_yearmonth.issue_count) + ','
            line_issue_arr += per_issue_yearmonth.yearmonth + ','
            line_issue_close_data += str(per_issue_yearmonth.close_issue_count) + ','

    pull_yearmonth = OsslibStatisticPullYearmonth.objects.filter(community_id=int(cid))
    line_pull_arr = ''
    line_pull_data = ''
    line_pull_merged_data = ''
    if pull_yearmonth.count() > 0:
        for per_pull_yearmonth in pull_yearmonth:
            line_pull_data += str(per_pull_yearmonth.pull_count) + ','
            line_pull_arr += per_pull_yearmonth.yearmonth + ','
            line_pull_merged_data += str(per_pull_yearmonth.merged_pull_count) + ','

    #developer
    developer_yearmonth = OsslibStatisticAuthorYearmonth.objects.filter(community_id=int(cid))
    line_developer_arr = ''
    line_developer_data = ''
    if developer_yearmonth.count() > 0:
        for per_developer_yearmonth in developer_yearmonth:
            line_developer_data += str(per_developer_yearmonth.developer_count) + ','
            line_developer_arr += per_developer_yearmonth.yearmonth + ','

    commit_hourday = OsslibStatisticCommitHourday.objects.filter(community_id=int(cid))
    commit_hourday_arr = ''
    if commit_hourday.count() > 0:
        for per_commit_hourday in commit_hourday:
            commit_hourday_str = str(per_commit_hourday.day) + '-' + str(per_commit_hourday.hour) + '-' + str(per_commit_hourday.commit_count)
            commit_hourday_arr += commit_hourday_str+','
    extra_info.update({'line_commit_arr': line_commit_arr})
    extra_info.update({'line_commit_data': line_commit_data})
    extra_info.update({'line_issue_arr': line_issue_arr})
    extra_info.update({'line_issue_data': line_issue_data})
    extra_info.update({'line_issue_close_data': line_issue_close_data})

    extra_info.update({'line_pull_arr': line_pull_arr})
    extra_info.update({'line_pull_data': line_pull_data})

    extra_info.update({'line_developer_arr': line_developer_arr})
    extra_info.update({'line_developer_data': line_developer_data})

    extra_info.update({'line_pull_merged_data': line_pull_merged_data})
    extra_info.update({'commit_hourday': commit_hourday_arr[:-1]})
    return render(request, 'commit.html', extra_info)

def issue(request):
    extra_info = dict()
    uid = request.session['user_id']

    community = get_nav_list(uid)
    extra_info.update(community)
    cid = request.GET.get('cid')
    try:
        page = request.GET.get('page')
    except:
        page = 1
    oss_id = []
    oss_list_id = OsslibCommunityList.objects.values("oss_id").filter(community_id=int(cid))
    for per_oss_id in oss_list_id:
        oss_id.append(int(per_oss_id['oss_id']))

    issue_all = OsslibIssue.objects.filter(oss_id__in=oss_id)[0:100]
    paginator = Paginator(issue_all, 20)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)

    issue_statistic = OsslibStatistic.objects.filter(community_id=int(cid))[0:1]
    issue_count = issue_statistic[0].issue_count
    issue_close_count = issue_statistic[0].issue_close_count
    issue_open_count = int(issue_count)-int(issue_close_count)

    extra_info.update({'issue': customer})
    extra_info.update({'cid': cid})
    extra_info.update({'issue_count': issue_count})
    extra_info.update({'issue_close_count': issue_close_count})
    extra_info.update({'issue_open_count': issue_open_count})
    return render(request, 'issue.html', extra_info)


def pull(request):
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    cid = request.GET.get('cid')
    try:
        page = request.GET.get('page')
    except:
        page = 1
    oss_id = []
    oss_list_id = OsslibCommunityList.objects.values("oss_id").filter(community_id=int(cid))
    for per_oss_id in oss_list_id:
        oss_id.append(int(per_oss_id['oss_id']))

    pulls_all = OsslibPulls.objects.filter(oss_id__in=oss_id)[0:100]
    paginator = Paginator(pulls_all, 20)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)

    pull_statistic = OsslibStatistic.objects.filter(community_id=int(cid))[0:1]
    pull_count = pull_statistic[0].pull_count
    pull_merged_count = pull_statistic[0].pull_merged_count
    pull_umerged_count = int(pull_count)-int(pull_merged_count)

    extra_info.update({'pull': customer})
    extra_info.update({'cid': cid})
    extra_info.update({'pull_count': pull_count})
    extra_info.update({'pull_merged_count': pull_merged_count})
    extra_info.update({'pull_umerged_count': pull_umerged_count})
    return render(request, 'pull.html', extra_info)

def author(request):
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    cid = request.GET.get('cid')
    author = OsslibStatisticAuthor.objects.filter(community_id=int(cid))
    extra_info.update({'author': author})
    oss_id = []
    oss_list_id = OsslibCommunityList.objects.values("oss_id",'oss_name').filter(community_id=int(cid))
    osslib_auth = dict()
    for per_oss_id in oss_list_id:
        osslib_auth_list = (OsslibAuthorList.objects.filter(oss_id=per_oss_id['oss_id'])[0:10])
        osslib_auth[per_oss_id['oss_name']]=osslib_auth_list
        oss_id.append(int(per_oss_id['oss_id']))
    extra_info.update({'osslib_auth': osslib_auth})
    oss_domain = OsslibDomain.objects.values("domain").filter(oss_id__in=oss_id).annotate(commits=Sum('commits'))[0:10]
    oss_domain_name = ''
    oss_domain_commit = ''
    for per_oss_domain in oss_domain:
        oss_domain_name += per_oss_domain['domain'] + ','
        oss_domain_commit += str(per_oss_domain['commits']) + ','
    extra_info.update({'oss_domain_name': oss_domain_name})
    extra_info.update({'oss_domain_commit': oss_domain_commit})
    return render(request, 'author.html', extra_info)