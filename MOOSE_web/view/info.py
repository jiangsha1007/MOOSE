from django.shortcuts import render,redirect
from django.http import HttpResponse
from model.community import *
from model.oss import *
from view.common import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum, Count
from operator import itemgetter
from django.http import JsonResponse
from influxdb_metrics.utils import query
from influxdb import InfluxDBClient
import time
import datetime
import statsmodels.api as sm
import pandas as pd
import math
import numpy as np

client = InfluxDBClient('192.168.3.14', 8086, 'moose', 'moose', 'moose')


def commit(request):
    extra_info = dict()
    uid = request.session['user_id']
    community = get_nav_list(uid)
    extra_info.update(community)
    cid = request.GET.get('cid')
    commit_yearmonth = MOOSEStatisticCommitYearmonth.objects.filter(community_id=int(cid))
    line_commit_arr = ''
    line_commit_data = ''
    line_issue_close_data = ''
    if commit_yearmonth.count() > 0:
        for per_commit_yearmonth in commit_yearmonth:
            line_commit_data += str(per_commit_yearmonth.commits_count) + ','
            line_commit_arr += per_commit_yearmonth.yearmonth + ','

    issue_yearmonth = MOOSEStatisticIssueYearmonth.objects.filter(community_id=int(cid))
    line_issue_arr = ''
    line_issue_data = ''
    if issue_yearmonth.count() > 0:
        for per_issue_yearmonth in issue_yearmonth:
            line_issue_data += str(per_issue_yearmonth.issue_count) + ','
            line_issue_arr += per_issue_yearmonth.yearmonth + ','
            line_issue_close_data += str(per_issue_yearmonth.close_issue_count) + ','

    pull_yearmonth = MOOSEStatisticPullYearmonth.objects.filter(community_id=int(cid))
    line_pull_arr = ''
    line_pull_data = ''
    line_pull_merged_data = ''
    if pull_yearmonth.count() > 0:
        for per_pull_yearmonth in pull_yearmonth:
            line_pull_data += str(per_pull_yearmonth.pull_count) + ','
            line_pull_arr += per_pull_yearmonth.yearmonth + ','
            line_pull_merged_data += str(per_pull_yearmonth.merged_pull_count) + ','

    #developer
    developer_yearmonth = MOOSEStatisticAuthorYearmonth.objects.filter(community_id=int(cid))
    line_developer_arr = ''
    line_developer_data = ''
    if developer_yearmonth.count() > 0:
        for per_developer_yearmonth in developer_yearmonth:
            line_developer_data += str(per_developer_yearmonth.developer_count) + ','
            line_developer_arr += per_developer_yearmonth.yearmonth + ','

    commit_hourday = MOOSEStatisticCommitHourday.objects.filter(community_id=int(cid))
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
    #client = InfluxDBClient('10.162.108.122', 8086, 'moose', 'moose', 'moose')
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
    oss_list_id = MOOSECommunityList.objects.values("oss_id").filter(community_id=int(cid))
    for per_oss_id in oss_list_id:
        oss_id.append(int(per_oss_id['oss_id']))

    issue_all = []
    result = client.query("select * from moose_issue where community_id='"+cid+"' order by time desc;").get_points()
    issue_index = 0
    for aa in result:
        if issue_index >=100:
            break
        issue_tmp = dict()
        issue_id = aa['issue_id']
        oss_id = aa['oss_id']
        oss_name = MOOSEMeta.objects.values('oss_fullname').filter(oss_id=oss_id)[0]['oss_fullname']
        if issue_id is None:
            continue
        issue_tmp.update({'issue_state': aa['issue_state']})
        issue_tmp.update({'issue_title': aa['title']})
        issue_tmp.update({'issue_body': aa['body']})
        issue_tmp.update({'id': aa['issue_id']})
        issue_tmp.update({'issue_create_time': aa['time']})
        issue_tmp.update({'issue_comment_count': aa['issue_comment_count']})
        issue_tmp.update({'oss_fullname': oss_name})
        issue_all.append(issue_tmp)
        issue_index += 1

    #issue_all = MOOSEIssue.objects.filter(oss_id__in=oss_id)[0:100]
    paginator = Paginator(issue_all, 20)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)

    issue_statistic = MOOSEStatistic.objects.filter(community_id=int(cid))[0:1]
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
    oss_list_id = MOOSECommunityList.objects.values("oss_id").filter(community_id=int(cid))
    for per_oss_id in oss_list_id:
        oss_id.append(int(per_oss_id['oss_id']))
    pulls_all = []
    result = client.query("select * from moose_pull where community_id='" + cid + "' order by time desc;").get_points()
    pull_index = 0
    for aa in result:
        if pull_index >= 100:
            break
        pull_tmp = dict()
        pull_id = aa['issue_id']
        oss_id = aa['oss_id']
        oss_name = MOOSEMeta.objects.values('oss_fullname').filter(oss_id=oss_id)[0]['oss_fullname']
        if pull_id is None:
            continue
        pull_tmp.update({'pull_state': aa['pull_state']})
        pull_tmp.update({'pull_is_merged': aa['pull_merged']})
        pull_tmp.update({'pull_title': aa['title']})
        pull_tmp.update({'pull_body': aa['body']})
        pull_tmp.update({'id': aa['issue_id']})
        pull_tmp.update({'pull_create_time': aa['time']})
        pull_tmp.update({'pull_comments': aa['pull_comment_count']})
        pull_tmp.update({'oss_fullname': oss_name})
        pulls_all.append(pull_tmp)
        pull_index += 1

    ##pulls_all = MOOSEPulls.objects.filter(oss_id__in=oss_id)[0:100]
    paginator = Paginator(pulls_all, 20)
    try:
        customer = paginator.page(page)
    except PageNotAnInteger:
        customer = paginator.page(1)

    pull_statistic = MOOSEStatistic.objects.filter(community_id=int(cid))[0:1]
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
    author = MOOSEStatisticAuthor.objects.filter(community_id=int(cid))
    extra_info.update({'author': author})
    oss_id = []
    oss_list_id = MOOSECommunityList.objects.values("oss_id", 'oss_name').filter(community_id=int(cid))
    MOOSE_auth = dict()
    for per_oss_id in oss_list_id:
        MOOSE_auth_list = (MOOSEAuthorList.objects.filter(oss_id=per_oss_id['oss_id'])[0:10])
        MOOSE_auth[per_oss_id['oss_name']] = MOOSE_auth_list
        oss_id.append(int(per_oss_id['oss_id']))
    print(MOOSE_auth)
    extra_info.update({'MOOSE_auth': MOOSE_auth})
    oss_domain = MOOSEDomain.objects.values("domain").filter(oss_id__in=oss_id).annotate(commits=Sum('commits'))[0:10]
    oss_domain_name = ''
    oss_domain_commit = ''
    for per_oss_domain in oss_domain:
        oss_domain_name += per_oss_domain['domain'] + ','
        oss_domain_commit += str(per_oss_domain['commits']) + ','
    extra_info.update({'oss_domain_name': oss_domain_name})
    extra_info.update({'oss_domain_commit': oss_domain_commit})
    return render(request, 'author.html', extra_info)

def monitor(request):
    extra_info = dict()
    uid = request.session['user_id']
    cid = request.GET.get('cid')
    community = get_nav_list(uid)
    extra_info.update(community)
    index_name = MOOSEIndex.objects.all()
    index_name_cal = MOOSEIndex.objects.filter(cal_need=1)
    result = client.query("select * from moose_index where oss_id='23418517' and index_type='IssueCommentEvent';").get_points()
    index_date = ''
    index_data = ''
    for aa in result:
        index_date += aa['time'][0:10] + ','
        index_data += str(aa['index_count']) + ','
    extra_info.update({'index_date': index_date})
    extra_info.update({'index_data': index_data})
    extra_info.update({'index_name': index_name})
    extra_info.update({'index_name_cal': index_name_cal})
    extra_info.update({'cid': cid})

    return render(request, 'index_monitor.html', extra_info)

def getIndex(request):
    result = client.query("select * from moose_index where oss_id='23418517' and index_type='IssueCommentEvent';").get_points()
    index_date = ''
    index_data = ''
    extra_info = dict()
    for aa in result:
        index_date += aa['time'][0:10] + ','
        index_data += str(aa['index_count']) + ','
    extra_info.update({'index_date': index_date})
    extra_info.update({'index_data': index_data})
    return JsonResponse(extra_info, safe=False)

def getMonitor(request):
    ids_str = request.POST.get('ids')
    cid = request.POST.get('cid')
    date_start = request.POST.get('date_start')
    date_end = request.POST.get('date_end')
    date_now = datetime.datetime.now()
    #获取今天的时间戳和预测7天后的时间戳
    date_now_str = (date_now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    date_pre_str = (date_now + datetime.timedelta(days=7)).strftime("%Y-%m-%d")

    #如果不指定起止时间，默认获取20天的数据
    if date_start == '' or date_start == None:
        date_start = (date_now + datetime.timedelta(days=-20)).strftime("%Y-%m-%d")
    if date_end == '' or date_end == None:
        date_end = (date_now + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    #获取时间的iso标准时间，便于查询时序数据库
    date_start_array = time.strptime(date_start, "%Y-%m-%d")
    date_start_stamp = int(time.mktime(date_start_array))
    date_start_ISO = datetime.datetime.fromtimestamp(date_start_stamp).isoformat()+"Z"
    date_end_array = time.strptime(date_end, "%Y-%m-%d")
    date_end_stamp = int(time.mktime(date_end_array))
    date_end_ISO = datetime.datetime.fromtimestamp(date_end_stamp).isoformat()+"Z"
    date_now_array = time.strptime(date_end, "%Y-%m-%d")
    date_now_stamp = int(time.mktime(date_now_array))
    date_now_ISO = datetime.datetime.fromtimestamp(date_now_stamp).isoformat() + "Z"

    ids_arr = ids_str.split(',')
    index_name_display = []
    index = []
    index_info = MOOSEIndex.objects.filter(id__in=ids_arr)
    extra_info = dict()
    ##计算自定义公式
    formula_customize = MOOSEIndex.objects.filter(community_id=cid, cal_need=2)#'(#W#*0.8)+(#F#*0.5+(#PR#*0.4))'
    for per_formula_customize in formula_customize:
        formula_customize_custormize = MOOSEIndexFormula.objects.values('cal_formula').filter(index_id=per_formula_customize.id)

        str_formula = formula_customize_custormize[0]['cal_formula']

        str_formula_new = str_formula.replace("+", "|").replace("-", "|").replace("*", "|").replace("(", "|").replace(")", "|");
        str_formula_arr = str_formula_new.split('|')
        result_cal = dict()
        cal_index_name = []
        for i in range(len(str_formula_arr)):
            if str_formula_arr[i] == '':
                continue
            if str_formula_arr[i].find('#') >= 0:
                #获取event名称
                event_name = MOOSEIndex.objects.values('index_name').filter(cal_name=str_formula_arr[i])
                result = client.query("select sum(index_count) from moose_index where community_id='" + str(cid) + "' and index_type = '" + event_name[0]['index_name'] + "' and (time >='" + date_start_ISO + "' and time <= '" + date_end_ISO + "') group by time(24h)  fill(0);").get_points()
                cal_index_name.append(str_formula_arr[i])
                index_cal_date = ''
                index_cal_data = ''
                index_cal = []
                for bb in result:
                    index_cal_date += bb['time'][0:10] + ','
                    index_cal_data += str(bb['sum']) + ','
                index_cal_date = index_cal_date[:-1]
                index_cal_data = index_cal_data[:-1]
                index_cal.append(index_cal_date.split(','))
                index_cal.append(index_cal_data.split(','))
                result_cal.update({str_formula_arr[i]: index_cal})
        date1 = datetime.datetime(date_start_array[0], date_start_array[1], date_start_array[2])
        date2 = datetime.datetime(date_end_array[0], date_end_array[1], date_end_array[2])
        diff_days = (date2 - date1).days
        for j in range(diff_days-2):
            str_formula_temp = str_formula
            for k in range(len(cal_index_name)):
                str_formula_temp = str_formula_temp.replace(cal_index_name[k], result_cal[cal_index_name[k]][1][j])
            index_cal_count = eval(str_formula_temp)
            body = [
                {
                    "measurement": "moose_index_customize",
                    "time": result_cal[cal_index_name[k]][0][j],
                    "tags": {
                        "oss_id": 0,
                        "community_id": 15,
                        "index_type": per_formula_customize.index_name
                    },
                    "fields": {
                        "index_count": index_cal_count
                    },
                }
            ]
            res = client.write_points(body)


    ######
    for per_index in index_info:
        moose_index_display = MOOSEIndexDisplay.objects.filter(index_id=per_index.id, community_id=cid)
        if moose_index_display.count()<=0:
            moose_index_display_new = MOOSEIndexDisplay()
            moose_index_display_new.index_id = per_index.id
            moose_index_display_new.community_id = cid
            moose_index_display_new.save()
        index_dict = dict()
        index_date = ''
        index_data = ''
        index_date_pre = ''
        index_data_pre = ''
        index_name_display.append(per_index.index_display)
        if per_index.cal_need == 2:
            result = client.query("select sum(index_count) from moose_index_customize where community_id='" + str(cid) + "' and index_type = '" + per_index.index_name + "' and (time >='" + date_start_ISO + "' and time <= '" + date_end_ISO + "') group by time(24h)  fill(0);").get_points()
        else:
            result = client.query("select sum(index_count) from moose_index where community_id='" + str(cid) + "' and index_type = '" + per_index.index_name + "' and (time >='" + date_start_ISO + "' and time <= '" + date_end_ISO + "') group by time(24h)  fill(0);").get_points()
        for aa in result:
            index_date += aa['time'][0:10] + ','
            index_data += str(aa['sum']) + ','
        #如果没有数据，默认全0
        if len(index_data) <= 0:
            date1 = datetime.datetime(date_start_array[0], date_start_array[1], date_start_array[2])
            date2 = datetime.datetime(date_end_array[0], date_end_array[1], date_end_array[2])
            diff_days = (date2 - date1).days

            for j in range(diff_days):
                index_date += (date_now + datetime.timedelta(days=(-diff_days + j + 1))).strftime("%Y-%m-%d")+','
                index_data += '0' + ','
        index_date = index_date[:-1]
        index_data = index_data[:-1]
        index_dict.update({'index_date': index_date})
        index_dict.update({'index_data': index_data})
        index_dict.update({'index_id': per_index.id})

        #获取全部数据用来预测,计算平均值及阈值
        index_date_pre_arr = []
        index_data_pre_arr = []
        average_count = 0
        if per_index.cal_need == 2:
            result_pre = client.query("select sum(index_count) from moose_index_customize where community_id='" + str(cid) + "' and index_type = '" + per_index.index_name + "' and (time <= '" + date_now_ISO + "') group by time(24h)  fill(0);").get_points()
        else:
            result_pre = client.query("select sum(index_count) from moose_index where community_id='" + str(
            cid) + "' and index_type = '" + per_index.index_name + "' and (time <= '" + date_now_ISO + "') group by time(24h)  fill(0);").get_points()
        for per_result_pre in result_pre:
            index_date_pre_arr.append(per_result_pre['time'][0:10])
            index_data_pre_arr.append(per_result_pre['sum'])

        try:
            pre_data = pd.DataFrame(index_data_pre_arr, index=index_date_pre_arr, columns=['Count'])
            pre_data['Timestamp'] = pd.to_datetime(index_date_pre_arr, format='%Y-%m-%d')
            pre_data.index = pre_data['Timestamp']
            pre_data = pre_data.resample('D').mean()

            try:
                fit1 = sm.tsa.statespace.SARIMAX(pre_data, order=(1, 1, 1), seasonal_order=(0, 1, 0, 12)).fit()
            except:
                fit1 = sm.tsa.statespace.SARIMAX(pre_data).fit()
            y_hat_avg = fit1.predict(start=date_now_str, end=date_pre_str,  dynamic=True)
            for j in range(len(y_hat_avg)-1):
                index_date_pre += (date_now + datetime.timedelta(days=(j+1))).strftime("%Y-%m-%d") + ','
                if y_hat_avg[j] < 0:
                    y_hat_avg[j] = 0
                index_data_pre += str(math.ceil(y_hat_avg[j])) + ','
        except:
            date1 = datetime.datetime(int(date_now_str[0:4]), int(date_now_str[5:7]), int(date_now_str[8:10]))
            date2 = datetime.datetime(int(date_pre_str[0:4]), int(date_pre_str[5:7]), int(date_pre_str[8:10]))
            diff_days = (date2 - date1).days
            for j in range(diff_days- 1):
                index_date_pre += (date_now + datetime.timedelta(days=(j + 1))).strftime("%Y-%m-%d") + ','
                index_data_pre += str(0) + ','
        index_dict.update({'index_date_pre': index_date_pre})
        index_dict.update({'index_data_pre': index_data_pre})
        upper_limit = pre_data['Count'].mean()+3*pre_data['Count'].std()
        lower_limit = pre_data['Count'].mean()-3*pre_data['Count'].std()
        index_dict.update({'upper_limit': upper_limit})
        index_dict.update({'lower_limit': lower_limit})

        index.append(index_dict)

        #计算平均值 阈值


    extra_info.update({'index_info': index})
    extra_info.update({'index_name': index_name_display})
    extra_info.update({'index_display_id': ids_arr})
    print(extra_info)
    return JsonResponse(extra_info, safe=False)


def addtoindex(request):
    cal_formula = request.POST.get('cal_formula')
    new_index_name = request.POST.get('index_name')
    cid = request.POST.get('cid')
    index_item = MOOSEIndex()
    index_item.index_name = new_index_name
    index_item.cal_need = 2
    index_item.community_id = cid
    index_item.index_display = new_index_name
    index_item.save()

    index_formula_item = MOOSEIndexFormula()
    index_formula_item.index_id = index_item.id
    index_formula_item.cal_formula = cal_formula
    index_formula_item.save()
    extra_info = dict()
    return HttpResponse('1', content_type='application/text')
