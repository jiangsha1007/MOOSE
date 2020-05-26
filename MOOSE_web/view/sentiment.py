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

client = InfluxDBClient('106.52.93.154', 8086, 'moose', 'moose', 'moose')


def sentiment(request):
    extra_info = dict()
    uid = request.session['user_id']
    cid = request.GET.get('cid')
    community = get_nav_list(uid, cid)
    extra_info.update(community)

    sentiment_type_yearmonth = MOOSEStatisticSentimentType.objects.filter(community_id=int(cid))
    sentiment_type_date = ''
    sentiment_type_debate = ''
    sentiment_type_bug = ''
    sentiment_type_confuse = ''
    sentiment_type_apologize = ''
    sentiment_type_third_party = ''
    sentiment_type_doc_standard = ''
    sentiment_type_work = ''
    sentiment_type_comment_id = ''


    #情感分类
    if sentiment_type_yearmonth.count() > 0:
        for per_sentiment_type_yearmonth in sentiment_type_yearmonth:
            sentiment_type_date += per_sentiment_type_yearmonth.yearmonth + ','
            #sentiment_type_debate += "{value:"+str(per_sentiment_type_yearmonth.debate)+",commit_id:'"+str(per_sentiment_type_yearmonth.comment_id)+"'}" + ','
            sentiment_type_debate += str(per_sentiment_type_yearmonth.debate) + ','
            sentiment_type_comment_id += str(per_sentiment_type_yearmonth.comment_id) + ','
            sentiment_type_bug += str(per_sentiment_type_yearmonth.bug) + ','
            sentiment_type_confuse += str(per_sentiment_type_yearmonth.confuse) + ','
            sentiment_type_apologize += str(per_sentiment_type_yearmonth.apologize) + ','
            sentiment_type_third_party += str(per_sentiment_type_yearmonth.third_party) + ','
            sentiment_type_doc_standard += str(per_sentiment_type_yearmonth.doc_standard) + ','
            sentiment_type_work += str(per_sentiment_type_yearmonth.work) + ','

    # 获取情感分析
    sentiment_yearmonth = MOOSEStatisticSentiment.objects.filter(community_id=int(cid))
    sentiment_date = ''
    sentiment_pos = ''
    sentiment_neg = ''
    sentiment_neu = ''
    sentiment_agv = ''
    if sentiment_yearmonth.count() > 0:
        for per_sentiment_yearmonth in sentiment_yearmonth:
            sentiment_date += per_sentiment_yearmonth.yearmonth + ','
            sentiment_pos += str(per_sentiment_yearmonth.pos) + ','
            sentiment_neg += str(per_sentiment_yearmonth.neg) + ','
            sentiment_neu += str(per_sentiment_yearmonth.neu) + ','
            if (per_sentiment_yearmonth.pos + per_sentiment_yearmonth.neg + per_sentiment_yearmonth.neu) != 0:
                sentiment_agv += str(round((per_sentiment_yearmonth.pos - per_sentiment_yearmonth.neg) / (
                        per_sentiment_yearmonth.pos + per_sentiment_yearmonth.neg + per_sentiment_yearmonth.neu),
                                           2)) + ','
            else:
                sentiment_agv += str(0) + ','

    extra_info.update({'sentiment_date': sentiment_date})
    extra_info.update({'sentiment_pos': sentiment_pos})
    extra_info.update({'sentiment_neg': sentiment_neg})
    extra_info.update({'sentiment_neu': sentiment_neu})
    extra_info.update({'sentiment_agv': sentiment_agv})

    extra_info.update({'sentiment_type_date': sentiment_type_date})
    extra_info.update({'sentiment_type_comment_id': sentiment_type_comment_id})
    extra_info.update({'sentiment_type_debate': sentiment_type_debate})
    extra_info.update({'sentiment_type_bug': sentiment_type_bug})
    extra_info.update({'sentiment_type_confuse': sentiment_type_confuse})
    extra_info.update({'sentiment_type_apologize': sentiment_type_apologize})
    extra_info.update({'sentiment_type_third_party': sentiment_type_third_party})
    extra_info.update({'sentiment_type_doc_standard': sentiment_type_doc_standard})
    extra_info.update({'sentiment_type_work': sentiment_type_work})
    extra_info.update({'path': 7})
    return render(request, 'sentiment.html', extra_info)

def sentiment_comment(request):
    comment_id = request.POST.get('comment_id')
    comment_ids = comment_id.split('|')
    comment_info = []
    for per_comment_id in comment_ids:
        comment_dict = dict()
        comment = MOOSEStatisticSentimentComment.objects.filter(comment_id=int(per_comment_id))
        if comment.count() > 0:
            for per_comment in comment:
                comment_dict["body"] = per_comment.comment_body
                comment_dict["user_name"] = per_comment.user_name
                comment_dict["user_id"] = per_comment.user_id
                comment_dict["oss_name"] = per_comment.oss_name
                comment_dict["oss_id"] = per_comment.oss_id
                comment_dict["issue_number"] = per_comment.issue_number
                comment_dict["create_time"] = per_comment.create_time
                comment_info.append(comment_dict)
    comment_json = json.dumps(comment_info, ensure_ascii=False)
    return HttpResponse(comment_json, content_type='application/json')