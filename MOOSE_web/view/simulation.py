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
from datetime import datetime
from datetime import timedelta

client = InfluxDBClient('106.52.93.154', 8086, 'moose', 'moose', 'moose')


def simulation(request):
    extra_info = dict()
    uid = request.session['user_id']
    cid = request.GET.get('cid')
    community = get_nav_list(uid, cid)
    extra_info.update(community)

    #获取模拟用户
    simulation_user_id = []
    simulation_user_name = []
    simulation_user = MOOSESimulation.objects.filter().values('user_id').annotate(Count=Count('user_id')).order_by('-Count')[:20]
    if simulation_user.count() > 0:
        for per_simulation_user in simulation_user:
            simulation_user_id.append(per_simulation_user['user_id'])
            user = MOOSEUser.objects.filter(user_id=per_simulation_user['user_id'])
            if user is not None:
                for per_user in user:
                    simulation_user_name
                    simulation_user_name.append(per_user.user_name)
            else:
                simulation_user_name.append('unknown')


    #获取模拟事件
    simulation_type_name = []
    simulation_type_name_display = []
    simulation_type = MOOSESimulationType.objects.all()
    if simulation_type.count() > 0:
        for per_simulation_type in simulation_type:
            simulation_type_name.append(per_simulation_type.event_name)
            simulation_type_name_display.append(per_simulation_type.event_display_name)

    #模拟预测
    simulation = dict()
    simulation_info = MOOSESimulation.objects.filter(user_id__in=simulation_user_id)
    if simulation_info.count() > 0:
        for per_simulation in simulation_info:
            user_id = per_simulation.user_id
            date = per_simulation.time
            event_type = per_simulation.eventType

            if user_id in simulation.keys():
                if date not in simulation[user_id].keys():
                    simulation[user_id][date] = dict()
            else:
                simulation[user_id] = dict()
                simulation[user_id][date] = dict()
            simulation[user_id][date][event_type] = per_simulation.count


    #模拟时间
    day_now = '2020-05-01'
    day_now_date = datetime.strptime(day_now, '%Y-%m-%d')

    simulation_date = []
    for i in range(30):
        day_now_date_next = day_now_date + timedelta(days=i)
        day_now_date_next_str = datetime.strftime(day_now_date_next, '%Y-%m-%d')
        simulation_date.append(day_now_date_next_str)

    simulation_all = []
    for user_id in simulation_user_id:
        simulation_result = []
        for i in range(30):
            simulation_result_user = dict()
            simulation_result_user['date'] = simulation_date[i]
            for type in simulation_type_name:
                if simulation_date[i] not in simulation[user_id]:
                    simulation_result_user[type] = 0
                else:
                    if type in simulation[user_id][simulation_date[i]]:
                        simulation_result_user[type] = (simulation[user_id][simulation_date[i]][type])
                    else:
                        simulation_result_user[type] = 0

            simulation_result.append(simulation_result_user)

        simulation_all.append(simulation_result)
        '''
        day_now_date_next_str = simulation_date[i]
        if day_now_date_next_str in simulation[user_id]:
            for type in simulation_type_name:
                if type in simulation[user_id][day_now_date_next_str]:
                    simulation_result_user[user_id][type] += str(simulation[user_id][day_now_date_next_str][type])+","
                else:
                    simulation_result_user[user_id][type] += '0,'
        else:
            for type in simulation_type_name:
                simulation_result_user[user_id][type] += '0,'
        '''

    extra_info.update({'simulation_date': simulation_date})
    extra_info.update({'simulation_user_name': simulation_user_name})
    extra_info.update({'simulation_user_id': simulation_user_id})
    extra_info.update({'simulation_type_name_display': simulation_type_name})
    extra_info.update({'simulation_result': simulation_all})
    extra_info.update({'path': 8})
    return render(request, 'simulation.html', extra_info)

