from model.common_model import *
from core.common_git import *
from core.datacollector import *
from core.common import *
from sqlobject import AND, OR,LIKE
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import os

import matplotlib.pyplot as plt
import pymysql
from apscheduler.schedulers.background import BlockingScheduler
import datetime
import openpyxl
from influxdb import InfluxDBClient
import time

import urllib.request as req


# 数据统计
class Statistics:

    def __init__(self):
        manager = get_thread_task_queue('statistics_queue')
        manager2 = get_thread_task_dict('statistics_dict')
        self.task_queue_basic = manager.statistics_queue()
        self.task_queue_issue = manager.statistics_queue()
        self.task_queue_pull = manager.statistics_queue()
        self.task_queue_commit = manager.statistics_queue()
        self.task_dict = manager2.statistics_dict()

    def oss_stat(self):
        community_info = MOOSECommunity.select()
        process_arg_info = []
        process_arg_info_all = []
        for per_community_info in community_info:
            community_id = per_community_info.id
            community_list_info = MOOSECommunityList.select(MOOSECommunityList.q.community_id == community_id)
            flag = 0
            for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == community_id):
                flag += 1
                statistic_info.community_id = community_id
                statistic_info.update_time = time.strftime('%Y-%m-%d')
            if flag == 0:
                item = dict()
                item['community_id'] = community_id
                item['update_time'] = time.strftime('%Y-%m-%d')
                MOOSEStatistic(**item)
            for per_community_list in community_list_info:
                process_info_tmp = []
                process_info_tmp.append(per_community_list.oss_id)
                process_info_tmp.append(per_community_list.community_id)
                process_arg_info_all.append(process_info_tmp)
            process_arg_info.append(per_community_list.community_id)

        #Basic data statistics
        #p1 = multiprocessing.Process(target=self._statistic_basic, args=(process_arg_info_all,))
        #p1.start()
        #issue data statistics
        #p = multiprocessing.Process(target=self._statistic_issue, args=(process_arg_info,))
        #p.start()
        # pull data statistics
        p = multiprocessing.Process(target=self._statistic_pull, args=(process_arg_info,))
        p.start()
        # commit data statistics
        #p = multiprocessing.Process(target=self._statistic_commit, args=(process_arg_info,))
        #p.start()
        # other data statisitcs
        #p = multiprocessing.Process(target=self._statistic_other, args=(process_arg_info_all,))
        #p.start()

        #p = multiprocessing.Process(target=self._statistic_issue_comment, args=(process_arg_info,))
        #p.start()
        p.join()
        exit(0)
        #pull data statistics

        #commit data statistics



        '''数据可视化 可删 2019.10.29 js
        wb = openpyxl.load_workbook('F:/code/python/osslib_core/MOOSE_core/core/1.xlsx')
        sht = wb.worksheets[0]  # 当前活跃的表单
        col_range = sht['C']
        index = 0
        # 定义需要用上的空数据数组，然后通过遍历数据库的数据将数据附上去
        xname = []
        ynum = []
        xname.append('0-500')
        xname.append('500-1000')
        xname.append('1000-1500')
        xname.append('1500-2000')
        xname.append('2000-2500')
        xname.append('2500-3000')
        xname.append('3000-3500')
        xname.append('3500-4000')
        xname.append('4000-4500')
        xname.append('4500-5000')
        xname.append('more than 5000')
        for index in range(0, 11):
            ynum.append(0)
        print (ynum)
        for cell in col_range:  # 打印BC两列单元格中的值内容
            index += 1
            if cell.value == 'repo_star':
                continue
            print(cell.value)
            num = int(cell.value)//500
            if num > 10:
                ynum[10] += 1
            else:
                ynum[num] += 1
        #创建一个figure（一个窗口）来显示条形图
        plt.figure(dpi=128,figsize=(10,6))
        plt.bar(xname,ynum)
        plt.xlabel('Number of Stars')
        plt.ylabel('Number')
        plt.xticks(xname, xname, rotation=30)
        for x,y in enumerate(ynum):
            plt.text(x,y+1,'%s'% y,ha='center')

        #创建一个figure（一个窗口）来显示折线图
        plt.figure()
        plt.plot(xname,ynum)
        for x,y in enumerate(ynum):
            plt.text(x,y,'%s'% y)

        #显示图表
        plt.show()



        
        exit(0)
        '''
    @staticmethod
    def _statistic_basic(q, ):
        basic_info = dict()
        for community_info in q:
            try:
                oss_id = community_info[0]
                community_id = community_info[1]
                oss_mata = MOOSEMetadata.select(MOOSEMetadata.q.oss_id == oss_id)[0]
                loc = oss_mata.oss_line_count
                if loc is None:
                    loc = 0
                doc = oss_mata.oss_developer_count
                if doc is None:
                    doc = 0
                foc = oss_mata.oss_file_count
                if foc is None:
                    foc = 0
                coc = oss_mata.oss_commit_count
                if coc is None:
                    coc = 0
                star_count = oss_mata.oss_star
                if star_count is None:
                    star_count = 0
                fork_count = oss_mata.oss_fork
                if fork_count is None:
                    fork_count = 0
                all_day = oss_mata.oss_all_day
                if all_day is None:
                    all_day = 0
                active_day = oss_mata.oss_active_day
                if active_day is None:
                    active_day = 0
                oss_language_count = oss_mata.oss_language_count
                if oss_language_count is None:
                    oss_language_count = 0
                if community_id in basic_info:
                    basic_info[community_id].update({'loc': basic_info[community_id]['loc']+loc})
                    basic_info[community_id].update({'doc': basic_info[community_id]['doc']+doc})
                    basic_info[community_id].update({'foc': basic_info[community_id]['foc']+foc})
                    basic_info[community_id].update({'coc': basic_info[community_id]['coc']+coc})
                    basic_info[community_id].update({'star_count': basic_info[community_id]['star_count']+star_count})
                    basic_info[community_id].update({'fork_count': basic_info[community_id]['fork_count']+fork_count})
                    basic_info[community_id].update({'all_day': basic_info[community_id]['all_day']+all_day})
                    basic_info[community_id].update({'active_day': basic_info[community_id]['active_day']+active_day})
                    basic_info[community_id].update({'oss_language_count': basic_info[community_id]['oss_language_count']+oss_language_count})
                else:
                    basic_info.update({community_id: dict()})
                    basic_info[community_id].update({'loc': loc})
                    basic_info[community_id].update({'doc': doc})
                    basic_info[community_id].update({'foc': foc})
                    basic_info[community_id].update({'coc': coc})
                    basic_info[community_id].update({'star_count': star_count})
                    basic_info[community_id].update({'fork_count': fork_count})
                    basic_info[community_id].update({'all_day': all_day})
                    basic_info[community_id].update({'active_day': active_day})
                    basic_info[community_id].update({'oss_language_count': oss_language_count})
            except Exception as ex:
                print(ex)
                pass
        for c_id in basic_info:
            for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == c_id):
                statistic_info.loc = basic_info[c_id]['loc']
                statistic_info.doc = basic_info[c_id]['doc']
                statistic_info.foc = basic_info[c_id]['foc']
                statistic_info.coc = basic_info[c_id]['coc']
                statistic_info.star_count = basic_info[c_id]['star_count']
                statistic_info.fork_count = basic_info[c_id]['fork_count']
                statistic_info.all_days = basic_info[c_id]['all_day']
                statistic_info.active_days = basic_info[c_id]['active_day']
                statistic_info.language_count = basic_info[c_id]['oss_language_count']


    @staticmethod
    def _statistic_issue(q,):
        client = InfluxDBClient('192.168.3.140', 8086, 'moose', 'moose', 'moose')
        for community_id in q:
            try:
                sql = "select * from moose_issue where community_id='"+str(community_id)+"';"
                result = client.query(sql).get_points()
                issue_count = 0
                issue_comment_count = 0
                issue_close_count = 0
                core_issue_count = 0
                issue_close_time = 0
                issue_open_monthyear = dict()
                issue_close_monthyear = dict()
                issue_monthyear = []
                for per_oss_issue in result:
                    issue_count += 1
                    if per_oss_issue['issue_comment_count'] is not None:
                        issue_comment_count += per_oss_issue['issue_comment_count']
                    if per_oss_issue['issue_state'] == 1:
                        issue_close_count += 1
                        if per_oss_issue['close_time'] is None or per_oss_issue['close_time'] == '':
                            per_oss_issue['close_time'] = datetime.datetime.now()
                        issue_close_time += time.mktime(
                            time.strptime(per_oss_issue['close_time'], "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(
                            time.strptime(per_oss_issue['time'], "%Y-%m-%dT%H:%M:%SZ"))

                        #statistic per month closed issues
                        close_at_month = per_oss_issue['close_time'][:7]
                        if close_at_month in issue_close_monthyear.keys():
                            issue_close_monthyear[close_at_month] += 1
                        else:
                            issue_close_monthyear[close_at_month] = 1
                        if close_at_month not in issue_monthyear:
                            issue_monthyear.append(close_at_month)
                    if per_oss_issue['core_issue'] == 1:
                        core_issue_count += 1

                    # statistic per month all issues
                    open_at_month = per_oss_issue['time'][:7]
                    if open_at_month in issue_open_monthyear.keys():
                        issue_open_monthyear[open_at_month] += 1
                    else:
                        issue_open_monthyear[open_at_month] = 1
                    if open_at_month not in issue_monthyear:
                        issue_monthyear.append(open_at_month)

                for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == community_id):
                    statistic_info.issue_count = issue_count
                    statistic_info.issue_close_count = issue_close_count
                    statistic_info.issue_comment_count = issue_comment_count
                    statistic_info.core_issue_count = core_issue_count
                    statistic_info.issue_close_time = issue_close_time/3600/24
                # 统计issue
                for issue_key in issue_monthyear:
                    moosestatisticyearmonth_issue = MOOSEStatisticIssueYearmonth.select(
                        AND(MOOSEStatisticIssueYearmonth.q.community_id == community_id,
                            MOOSEStatisticIssueYearmonth.q.yearmonth == issue_key))
                    if moosestatisticyearmonth_issue.count() > 0:
                        for per_moosestatisticyearmonth_issue in moosestatisticyearmonth_issue:
                            if issue_key in issue_open_monthyear:
                                per_moosestatisticyearmonth_issue.issue_count = issue_open_monthyear[issue_key]
                            else:
                                per_moosestatisticyearmonth_issue.issue_count = 0
                            if issue_key in issue_close_monthyear:
                                per_moosestatisticyearmonth_issue.close_issue_count = issue_close_monthyear[issue_key]
                            else:
                                per_moosestatisticyearmonth_issue.close_issue_count = 0
                    else:
                        item = dict()
                        item['community_id'] = community_id
                        item['yearmonth'] = issue_key
                        if issue_key in issue_open_monthyear:
                            item['issue_count'] = issue_open_monthyear[issue_key]
                        else:
                            item['issue_count'] = 0
                        if issue_key in issue_close_monthyear:
                            item['close_issue_count'] = issue_close_monthyear[issue_key]
                        else:
                            item['close_issue_count'] = 0
                        MOOSEStatisticIssueYearmonth(**item)

            except Exception as ex:
                print(ex)
                pass

    @staticmethod
    def _statistic_issue_comment(q,):
        client = InfluxDBClient('192.168.3.140', 8086, 'moose', 'moose', 'moose')
        for community_id in q:
            try:
                sql = "select * from moose_issue_comment where community_id='"+str(community_id)+"';"
                result = client.query(sql).get_points()
                issue_comment_count = 0
                core_issue_comment_count = 0
                issue_comment_monthyear = []
                sentiment_pos = dict()
                sentiment_neg = dict()
                sentiment_neu = dict()
                sentiment_avg = dict()
                sentiment_monthyear = []
                sid = SentimentIntensityAnalyzer()
                for per_oss_issue_comment in result:
                    core_issue_comment_count += 1
                    # 分析comment情感

                    creat_month = per_oss_issue_comment['time'][:7]
                    issue_comment_body = per_oss_issue_comment['body']
                    label = sid.polarity_scores(issue_comment_body)['compound']
                    if label >= 0.3:
                        if creat_month in sentiment_pos:
                            sentiment_pos[creat_month] = sentiment_pos[creat_month] + 1
                        else:
                            sentiment_pos[creat_month] = 1
                    if label <= -0.3:
                        if creat_month in sentiment_neg:
                            sentiment_neg[creat_month] = sentiment_neg[creat_month] + 1
                        else:
                            sentiment_neg[creat_month] = 1
                    if label < 0.3 and label > -0.3:
                        if creat_month in sentiment_neu:
                            sentiment_neu[creat_month] = sentiment_neu[creat_month] + 1
                        else:
                            sentiment_neu[creat_month] = 1
                    if creat_month not in sentiment_monthyear:
                        sentiment_monthyear.append(creat_month)
                for sentiment_key in sentiment_monthyear:
                    moosestatisticsentimentyearmonth = MOOSEStatisticSentiment.select(
                        AND(MOOSEStatisticSentiment.q.community_id == community_id,
                            MOOSEStatisticSentiment.q.yearmonth == sentiment_key))
                    if moosestatisticsentimentyearmonth.count() > 0:
                        for per_moosestatisticsentimentyearmonth in moosestatisticsentimentyearmonth:
                            if sentiment_key in sentiment_pos:
                                per_moosestatisticsentimentyearmonth.pos = sentiment_pos[sentiment_key]
                            if sentiment_key in sentiment_neg:
                                per_moosestatisticsentimentyearmonth.neg = sentiment_neg[sentiment_key]
                            if sentiment_key in sentiment_neu:
                                per_moosestatisticsentimentyearmonth.neu = sentiment_neu[sentiment_key]
                    else:
                        item = dict()
                        item['community_id'] = int(community_id)
                        item['yearmonth'] = sentiment_key
                        if sentiment_key in sentiment_pos:
                            item['pos'] = sentiment_pos[sentiment_key]
                        else:
                            item['pos'] = 0
                        if sentiment_key in sentiment_neg:
                            item['neg'] = sentiment_neg[sentiment_key]
                        else:
                            item['neg'] = 0
                        if sentiment_key in sentiment_neg:
                            item['neu'] = sentiment_neu[sentiment_key]
                        else:
                            item['neu'] = 0
                        MOOSEStatisticSentiment(**item)

                for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == community_id):
                    statistic_info.core_issue_comment_count = core_issue_comment_count
                ''''
                # 统计issue
                for issue_key in issue_monthyear:
                    moosestatisticyearmonth_issue = MOOSEStatisticIssueYearmonth.select(
                        AND(MOOSEStatisticIssueYearmonth.q.community_id == community_id,
                            MOOSEStatisticIssueYearmonth.q.yearmonth == issue_key))
                    if moosestatisticyearmonth_issue.count() > 0:
                        for per_moosestatisticyearmonth_issue in moosestatisticyearmonth_issue:
                            if issue_key in issue_open_monthyear:
                                per_moosestatisticyearmonth_issue.issue_count = issue_open_monthyear[issue_key]
                            else:
                                per_moosestatisticyearmonth_issue.issue_count = 0
                            if issue_key in issue_close_monthyear:
                                per_moosestatisticyearmonth_issue.close_issue_count = issue_close_monthyear[issue_key]
                            else:
                                per_moosestatisticyearmonth_issue.close_issue_count = 0
                    else:
                        item = dict()
                        item['community_id'] = community_id
                        item['yearmonth'] = issue_key
                        if issue_key in issue_open_monthyear:
                            item['issue_count'] = issue_open_monthyear[issue_key]
                        else:
                            item['issue_count'] = 0
                        if issue_key in issue_close_monthyear:
                            item['close_issue_count'] = issue_close_monthyear[issue_key]
                        else:
                            item['close_issue_count'] = 0
                        MOOSEStatisticIssueYearmonth(**item)
                '''

            except Exception as ex:
                print(ex)
                pass

    @staticmethod
    def _statistic_pull(q,):
        client = InfluxDBClient('192.168.3.140', 8086, 'moose', 'moose', 'moose')
        for community_id in q:
            pull_count = 0
            pull_merged_count = 0
            pull_comment_count = 0
            pull_review_count = 0
            core_review_count = 0
            pull_review_comment_count = 0
            core_review_comment_count = 0
            core_pull_count = 0
            pull_merged_time = 0
            pull_open_monthyear = dict()
            pull_merged_monthyear = dict()
            pull_monthyear = []
            core_developer = []
            try:
                sql = "select * from moose_pull where community_id='" + str(community_id) + "';"
                result = client.query(sql).get_points()
                for per_oss_pull in result:
                    pull_count += 1
                    if per_oss_pull['user_id'] in core_developer:
                        pass
                    else:
                        core_developer.append(per_oss_pull['user_id'])
                    if per_oss_pull['pull_merged'] == 1:
                        pull_merged_count += 1
                        if per_oss_pull['merged_time'] is None or per_oss_pull['merged_time'] == '':
                            per_oss_pull['merged_time'] = datetime.datetime.now()
                        pull_merged_time += time.mktime(
                            time.strptime(per_oss_pull['merged_time'], "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(
                            time.strptime(per_oss_pull['time'], "%Y-%m-%dT%H:%M:%SZ"))
                        # statistic per month closed pulls
                        merged_at_month = per_oss_pull['merged_time'][:7]
                        if merged_at_month in pull_merged_monthyear.keys():
                            pull_merged_monthyear[merged_at_month] += 1
                        else:
                            pull_merged_monthyear[merged_at_month] = 1
                        if merged_at_month not in pull_monthyear:
                            pull_monthyear.append(merged_at_month)
                    # statistic per month all pulls
                    open_at_month = per_oss_pull['time'][:7]
                    if open_at_month in pull_open_monthyear.keys():
                        pull_open_monthyear[open_at_month] += 1
                    else:
                        pull_open_monthyear[open_at_month] = 1
                    if open_at_month not in pull_monthyear:
                        pull_monthyear.append(open_at_month)

                    if per_oss_pull['pull_comment_count'] is not None:
                        pull_comment_count += per_oss_pull['pull_comment_count']
                    if per_oss_pull['pull_review_comment_count'] is not None:
                        pull_review_comment_count += per_oss_pull['pull_review_comment_count']
                    if per_oss_pull['pull_reviewed'] == 1:
                        pull_review_count += 1
                    if per_oss_pull['core_review_count'] is not None:
                        core_review_count += per_oss_pull['core_review_count']
                    if per_oss_pull['core_review_comment_count'] is not None:
                        core_review_comment_count += per_oss_pull['core_review_comment_count']
                    if per_oss_pull['core_pull'] is not None:
                        core_pull_count += 1
                for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == community_id):
                    statistic_info.pull_count = pull_count
                    statistic_info.pull_merged_count = pull_merged_count
                    statistic_info.pull_comment_count = pull_comment_count
                    statistic_info.pull_review_count = pull_review_count
                    statistic_info.core_review_count = core_review_count
                    statistic_info.pull_review_comment_count = pull_review_comment_count
                    statistic_info.core_review_comment_count = core_review_comment_count
                    statistic_info.core_pull_count = core_pull_count
                    statistic_info.pull_merged_time = pull_merged_time/3600/24
                    statistic_info.core_developer_count = len(core_developer)
                    # 统计issue
                    for pull_key in pull_monthyear:
                        moosestatisticyearmonth_pull = MOOSEStatisticPullYearmonth.select(
                            AND(MOOSEStatisticPullYearmonth.q.community_id == community_id,
                                MOOSEStatisticPullYearmonth.q.yearmonth == pull_key))
                        if moosestatisticyearmonth_pull.count() > 0:
                            for per_moosestatisticyearmonth_pull in moosestatisticyearmonth_pull:
                                if pull_key in pull_open_monthyear:
                                    per_moosestatisticyearmonth_pull.issue_count = pull_open_monthyear[pull_key]
                                else:
                                    per_moosestatisticyearmonth_pull.issue_count = 0
                                if pull_key in pull_merged_monthyear:
                                    per_moosestatisticyearmonth_pull.close_issue_count = pull_merged_monthyear[pull_key]
                                else:
                                    per_moosestatisticyearmonth_pull.close_issue_count = 0
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['yearmonth'] = pull_key
                            if pull_key in pull_open_monthyear:
                                item['pull_count'] = pull_open_monthyear[pull_key]
                            else:
                                item['pull_count'] = 0
                            if pull_key in pull_merged_monthyear:
                                item['merged_pull_count'] = pull_merged_monthyear[pull_key]
                            else:
                                item['merged_pull_count'] = 0
                            MOOSEStatisticPullYearmonth(**item)

            except Exception as ex:
                print(ex)
                pass

    @staticmethod
    def _statistic_commit(q, ):
        client = InfluxDBClient('192.168.3.140', 8086, 'moose', 'moose', 'moose')
        for community_id in q:
            try:
                commit_monthyear = dict()
                commit_count = 0
                comment_count = 0
                core_comment_count = 0
                sql = "select * from moose_commit where community_id='" + str(community_id) + "';"
                result = client.query(sql).get_points()
                for per_oss_commit in result:
                    commit_count += 1
                    # statistic per month all issues
                    commit_at_month = per_oss_commit['time'][:7]
                    if commit_at_month in commit_monthyear.keys():
                        commit_monthyear[commit_at_month] += 1
                    else:
                        commit_monthyear[commit_at_month] = 1
                # 统计commit
                for commit_key in commit_monthyear:
                    moosestatisticyearmonth_commit = MOOSEStatisticCommitYearmonth.select(
                        AND(MOOSEStatisticCommitYearmonth.q.community_id == community_id,
                            MOOSEStatisticCommitYearmonth.q.yearmonth == commit_key))
                    if moosestatisticyearmonth_commit.count() > 0:
                        for per_moosestatisticyearmonth_commit in moosestatisticyearmonth_commit:
                            per_moosestatisticyearmonth_commit.commits_count = commit_monthyear[commit_key]
                    else:
                        item = dict()
                        item['community_id'] = community_id
                        item['yearmonth'] = commit_key
                        item['commits_count'] = commit_monthyear[commit_key]
                        MOOSEStatisticCommitYearmonth(**item)
                sql = "select * from moose_comment where community_id='" + str(community_id) + "';"
                result = client.query(sql).get_points()
                for per_oss_comment in result:
                    if per_oss_comment['core_commit_comment'] is not None:
                        core_comment_count += per_oss_comment['core_commit_comment']
                    comment_count += 1
                for statistic_info in MOOSEStatistic.select(MOOSEStatistic.q.community_id == community_id):
                    statistic_info.commit_count = commit_count
                    statistic_info.commit_comment_count = comment_count
                    statistic_info.core_commit_comment_count = core_comment_count
            except Exception as ex:
                print(ex)

    @staticmethod
    def _statistic_other(q, ):
        basic_info = dict()
        for community_info in q:
            try:
                oss_id = community_info[0]
                community_id = community_info[1]
                oss_commit_hourday = MOOSEActivityHourOfWeek.select(MOOSEActivityHourOfWeek.q.oss_id == oss_id)
                # commit hourday statistic
                day_week = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
                if oss_commit_hourday.count() > 0:
                    for per_oss_commit_hourday in oss_commit_hourday:
                        day = per_oss_commit_hourday.weekday_hour[:3]
                        day_index = day_week.index(day)
                        hour = int(per_oss_commit_hourday.weekday_hour[4:])
                        moosestatistichourday_commit = MOOSEStatisticCommitHourday.select(
                            AND(MOOSEStatisticCommitHourday.q.community_id == community_id,
                                MOOSEStatisticCommitHourday.q.day == day_index,
                                MOOSEStatisticCommitHourday.q.hour == hour))
                        if moosestatistichourday_commit.count() > 0:
                            for per_moosestatistichourday_commit in moosestatistichourday_commit:
                                per_moosestatistichourday_commit.commit_count = int(
                                    per_moosestatistichourday_commit.commit_count) + int(per_oss_commit_hourday.commits)
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['day'] = int(day_index)
                            item['hour'] = int(hour)
                            item['commit_count'] = int(per_oss_commit_hourday.commits)
                            MOOSEStatisticCommitHourday(**item)
                oss_author = MOOSEAuthorCumulated.select(MOOSEAuthorCumulated.q.oss_id == oss_id).orderBy('-date')
                oss_author_arr = []
                flag = 0
                if oss_author:
                    for per_oss_author in oss_author:
                        if flag < 6:
                            if per_oss_author.author not in oss_author_arr:
                                name = per_oss_author.author
                                user = MOOSEUser.select(OR(MOOSEUser.q.user_fullname == name,
                                                            LIKE(MOOSEUser.q.user_fullname, '%' + name + '%')))
                                print(user)
                                try:
                                    if user.count() > 0:
                                        user_id = user[0].user_id
                                        file_name = 'F:\\code\\python\\MOOSE\\MOOSE_web\\static\\img\\avatar\\' + str(user_id) + '.png'
                                        try:
                                            if os.path.isfile(file_name):
                                                avatar_url = user[0].avatar_url
                                        #urllib.request.urlretrieve(avatar_url, filename=file_name)
                                                with req.urlopen(avatar_url) as d, open(file_name, "wb") as opfile:
                                                    data = d.read()
                                                    opfile.write(data)
                                        except:
                                            req.urlretrieve(avatar_url, filename=file_name)
                                    else:
                                        user_id = 0
                                except BaseException as ex:
                                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
                                    #r = urllib.request(url=avatar_url, headers=headers)
                                    #r = requests.get(avatar_url)
                                    ##with open(file_name, 'wb') as f:
                                    #    f.write(r.content)
                                    print(ex)
                                    user_id = 0
                                oss_author_arr.append(name)
                                author_commit = MOOSEAuthorCumulated.select(MOOSEAuthorCumulated.q.author == name).orderBy('-cumulated_commits')[0]
                                moosestatisticauthor = MOOSEStatisticAuthor.select(
                                    AND(MOOSEStatisticAuthor.q.oss_id == oss_id,
                                        MOOSEStatisticAuthor.q.user_id == user_id,
                                        MOOSEStatisticAuthor.q.user_name == name))
                                if moosestatisticauthor.count() > 0:
                                    for per_moosestatisticauthor in moosestatisticauthor:
                                        per_moosestatisticauthor.commit_count = int(author_commit.cumulated_commits)
                                        per_moosestatisticauthor.last_commit_time = author_commit.date
                                else:
                                    item = dict()
                                    item['community_id'] = community_id
                                    item['oss_id'] = int(oss_id)
                                    item['commit_count'] = int(author_commit.cumulated_commits)
                                    item['last_commit_time'] = author_commit.date
                                    item['user_id'] = user_id
                                    item['user_name'] = name
                                    MOOSEStatisticAuthor(**item)
                                flag = flag + 1

                oss_developer = MOOSEAuthorMonth.select(MOOSEAuthorMonth.q.oss_id == oss_id)
                if oss_developer:
                    for per_oss_developer in oss_developer:
                        moosestatisticauthyearmonth = MOOSEStatisticAuthorYearmonth.select(
                            AND(MOOSEStatisticAuthorYearmonth.q.community_id == community_id,
                                MOOSEStatisticAuthorYearmonth.q.yearmonth == per_oss_developer.month))
                        if moosestatisticauthyearmonth.count() > 0:
                            for per_moosestatisticauthyearmonth in moosestatisticauthyearmonth:
                                per_moosestatisticauthyearmonth.developer_count = per_moosestatisticauthyearmonth.developer_count + per_oss_developer.author_number
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['yearmonth'] = per_oss_developer.month
                            item['developer_count'] = per_oss_developer.author_number
                            MOOSEStatisticAuthorYearmonth(**item)
                        # user = OsslibUser.select(OsslibUser)

            except Exception as ex:
                print(ex)


    '''
    @staticmethod

    
    def _statistic(q, i, lock):

        while True:
            if q.empty():
                break
            try:
                info = q.get()
                oss_id = info[0]
                community_id = info[1]
                statistic_id = info[2]
                oss_mata = MOOSEMetadata.select(MOOSEMetadata.q.oss_id == oss_id)[0]
                loc = oss_mata.oss_line_count
                doc = oss_mata.oss_developer_count
                foc = oss_mata.oss_file_count
                coc = oss_mata.oss_commit_count
                star_count = oss_mata.oss_star
                fork_count = oss_mata.oss_fork
                all_day = oss_mata.oss_all_day
                active_day = oss_mata.oss_active_day

            except:
                pass
            print(basic_info)
            exit(0)
                #oss_commit = OsslibActivityYearMonth.select(OsslibActivityYearMonth.q.oss_id == oss_mata.oss_id)
                #oss_issue = OsslibIssue.select(OsslibIssue.q.oss_id == oss_mata.oss_id)
                #oss_pull = OsslibPulls.select(OsslibPulls.q.oss_id == oss_mata.oss_id)
                #oss_commit_hourday = OsslibActivityHourOfWeek.select(OsslibActivityHourOfWeek.q.oss_id == oss_mata.oss_id)
                #oss_developer = OsslibAuthorMonth.select(OsslibAuthorMonth.q.oss_id == oss_mata.oss_id)
                oss_issue_comment =OsslibIssueComment.select(OsslibIssueComment.q.oss_id == oss_mata.oss_id)
                
                oss_author = OsslibAuthorCumulated.select(OsslibAuthorCumulated.q.oss_id == oss_mata.oss_id).orderBy('-date')
                oss_author_arr = []
                flag = 0
                if oss_author:
                    for per_oss_author in oss_author:
                        if flag < 6:
                            if per_oss_author.author not in oss_author_arr:
                                name = per_oss_author.author
                                user = OsslibUser.select(OR(OsslibUser.q.user_fullname == name,LIKE(OsslibUser.q.user_fullname,'%'+name+'%')))
                                print(user)
                                try:
                                    if user:
                                        user_id = user[0].user_id
                                        file_name = 'F:\\code\\python\\OSSlib_web\\OSSlibary_web\\static\\img\\avatar\\' + str(user_id) + '.png'
                                        if os.path.isfile(file_name):
                                            avatar_url = user[0].avatar_url
                                        r = requests.get(avatar_url)
                                        with open(file_name, 'wb') as f:
                                            f.write(r.content)
                                except BaseException as ex :
                                    print(ex)
                                    user_id = 0
                                oss_author_arr.append(name)
                                author_commit = OsslibAuthorCumulated.select(OsslibAuthorCumulated.q.author == name).orderBy('-cumulated_commits')[0]
                                item = dict()
                                item['community_id'] = community_id
                                item['oss_id'] = int(oss_mata.oss_id)
                                item['commit_count'] = int(author_commit.cumulated_commits)
                                item['last_commit_time'] = author_commit.date
                                item['user_id'] = user_id
                                item['user_name'] = name
                                #OsslibStatisticAuthor(**item)
                                flag = flag + 1
                        #user = OsslibUser.select(OsslibUser)
                print(oss_author)
                
                #分析comment情感
                sentiment_pos = dict()
                sentiment_neg = dict()
                sentiment_neu = dict()
                sentiment_avg = dict()
                sentiment_monthyear = []
                sid = SentimentIntensityAnalyzer()
                for per_issue_comment in oss_issue_comment:

                    creat_month = per_issue_comment.created_time[:7]
                    issue_comment_body = per_issue_comment.body
                    label = sid.polarity_scores(issue_comment_body)['compound']
                    if label >= 0.5:
                        if creat_month in sentiment_pos:
                            sentiment_pos[creat_month] = sentiment_pos[creat_month] + 1
                        else:
                            sentiment_pos[creat_month] = 1
                    if label <= -0.5:
                        if creat_month in sentiment_neg:
                            sentiment_neg[creat_month] = sentiment_neg[creat_month] + 1
                        else:
                            sentiment_neg[creat_month] = 1
                    if label < 0.5 and label > -0.5:
                        if creat_month in sentiment_neu:
                            sentiment_neu[creat_month] = sentiment_neu[creat_month] + 1
                        else:
                            sentiment_neu[creat_month] = 1
                    if creat_month not in sentiment_monthyear:
                        sentiment_monthyear.append(creat_month)


                
                #分析issue
                issue_count = 0
                issue_close_count = 0
                issue_close_time = 0
                core_issue_count = 0
                issue_open_monthyear = dict()
                issue_close_monthyear = dict()
                issue_monthyear = []
                issue_comment_count = 0
                if oss_issue:
                    for per_oss_issue in oss_issue:
                        issue_count += 1
                        #统计月份
                        open_at_month = per_oss_issue.issue_create_time[:7]
                        if open_at_month in issue_open_monthyear.keys():
                            issue_open_monthyear[open_at_month] += 1
                        else:
                            issue_open_monthyear[open_at_month] = 1
                        if open_at_month not in issue_monthyear:
                            issue_monthyear.append(open_at_month)
                        if per_oss_issue.issue_state == 1:
                            issue_close_count += 1
                            close_at = per_oss_issue.issue_close_time
                            open_at = per_oss_issue.issue_create_time
                            issue_close_time += time.mktime(
                                time.strptime(close_at, "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(
                                time.strptime(open_at, "%Y-%m-%dT%H:%M:%SZ"))
                            close_at_month = per_oss_issue.issue_close_time[:7]
                            if close_at_month in issue_close_monthyear.keys():
                                issue_close_monthyear[close_at_month] += 1
                            else:
                                issue_close_monthyear[close_at_month] = 1
                            if close_at_month not in issue_monthyear:
                                issue_monthyear.append(close_at_month)
                        if per_oss_issue.issue_user_type =='MEMBER' or per_oss_issue.issue_user_type =='COLLABORATOR':
                            core_issue_count += 1
                        issue_comment_count += per_oss_issue.issue_comment_count
                #分析pull
                pull_count = 0
                pull_comment_count = 0
                pull_review_comment_count = 0
                pull_review_count = 0
                core_pull_count = 0
                pull_merged_count = 0
                pull_merged_time = 0
                core_developer = []
                core_developer_count = 0
                pull_open_monthyear = dict()
                pull_merged_monthyear = dict()
                pull_monthyear = []
                if oss_pull:
                    for per_oss_pull in oss_pull:
                        # 统计月份
                        open_at_month = per_oss_pull.pull_create_time[:7]
                        if open_at_month in pull_open_monthyear.keys():
                            pull_open_monthyear[open_at_month] = pull_open_monthyear[open_at_month] + 1
                        else:
                            pull_open_monthyear[open_at_month] = 1
                        if open_at_month not in pull_monthyear:
                            pull_monthyear.append(open_at_month)
                        pull_count += 1
                        pull_comment_count += per_oss_pull.pull_comments
                        pull_review_comment_count += per_oss_pull.review_comments
                        if per_oss_pull.pull_is_reviewed == 1:
                            pull_review_count += 1
                        if per_oss_pull.pull_is_merged == 1:
                            pull_merged_count += 1
                            merged_at = per_oss_pull.pull_merged_time
                            create_at = per_oss_pull.pull_create_time
                            pull_merged_time += time.mktime(
                                time.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(
                                time.strptime(create_at, "%Y-%m-%dT%H:%M:%SZ"))
                            merged_at_month = per_oss_pull.pull_merged_time[:7]
                            if merged_at_month in pull_merged_monthyear.keys():
                                pull_merged_monthyear[merged_at_month] = pull_merged_monthyear[merged_at_month] + 1
                            else:
                                pull_merged_monthyear[merged_at_month] = 1
                            if merged_at_month not in pull_monthyear:
                                pull_monthyear.append(merged_at_month)
                        if per_oss_pull.pull_author_association =='MEMBER' or per_oss_pull.pull_author_association =='COLLABORATOR':
                            core_pull_count += 1
                            if per_oss_pull.user_id in core_developer:
                                pass
                            else:
                                core_developer.append(per_oss_pull.user_id)
                                core_developer_count += 1
                
                lock.acquire()
                #统计情感
                for sentiment_key in sentiment_monthyear:
                    osslibstatisticsentimentyearmonth = OsslibStatisticSentiment.select(
                        AND(OsslibStatisticSentiment.q.community_id == community_id,
                            OsslibStatisticSentiment.q.yearmonth == sentiment_key))
                    if osslibstatisticsentimentyearmonth.count() > 0:
                        for per_osslibstatisticsentimentyearmonth in osslibstatisticsentimentyearmonth:
                            if sentiment_key in sentiment_pos:
                                per_osslibstatisticsentimentyearmonth.pos = per_osslibstatisticsentimentyearmonth.pos + \
                                                                           sentiment_pos[sentiment_key]
                            if sentiment_key in sentiment_neg:
                                per_osslibstatisticsentimentyearmonth.neg = per_osslibstatisticsentimentyearmonth.neg + \
                                                                                 sentiment_neg[sentiment_key]
                            if sentiment_key in sentiment_neu:
                                per_osslibstatisticsentimentyearmonth.neu = per_osslibstatisticsentimentyearmonth.neu + \
                                                                                 sentiment_neu[sentiment_key]
                    else:
                        item = dict()
                        item['community_id'] = int(community_id)
                        item['yearmonth'] = sentiment_key
                        if sentiment_key in sentiment_pos:
                            item['pos'] = sentiment_pos[sentiment_key]
                        else:
                            item['pos'] = 0
                        if sentiment_key in sentiment_neg:
                            item['neg'] = sentiment_neg[sentiment_key]
                        else:
                            item['neg'] = 0
                        if sentiment_key in sentiment_neg:
                            item['neu'] = sentiment_neu[sentiment_key]
                        else:
                            item['neu'] = 0
                        OsslibStatisticSentiment(**item)
                #统计每月developer
                
                if oss_developer:
                    for per_oss_developer in oss_developer:
                        osslibstatisticauthyearmonth = OsslibStatisticAuthorYearmonth.select(
                            AND(OsslibStatisticAuthorYearmonth.q.community_id == community_id,
                                OsslibStatisticAuthorYearmonth.q.yearmonth == per_oss_developer.month))
                        if osslibstatisticauthyearmonth.count() > 0:
                            for per_osslibstatisticauthyearmonth in osslibstatisticauthyearmonth:
                                per_osslibstatisticauthyearmonth.developer_count = per_osslibstatisticauthyearmonth.developer_count + per_oss_developer.author_number
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['yearmonth'] = per_oss_developer.month
                            item['developer_count'] = per_oss_developer.author_number
                            OsslibStatisticAuthorYearmonth(**item)
                #统计issue
                for issue_key in issue_monthyear:
                    osslibstatisticyearmonth = OsslibStatisticIssueYearmonth.select(
                        AND(OsslibStatisticIssueYearmonth.q.community_id == community_id,
                            OsslibStatisticIssueYearmonth.q.yearmonth == issue_key))
                    if osslibstatisticyearmonth.count() > 0:
                        for per_osslibstatisticyearmonth in osslibstatisticyearmonth:
                            if issue_key in issue_open_monthyear:
                                per_osslibstatisticyearmonth.issue_count = per_osslibstatisticyearmonth.issue_count + issue_open_monthyear[issue_key]
                            if issue_key in issue_close_monthyear:
                                per_osslibstatisticyearmonth.close_issue_count = per_osslibstatisticyearmonth.close_issue_count + issue_close_monthyear[issue_key]
                    else:
                        item = dict()
                        item['community_id'] = community_id
                        item['yearmonth'] = issue_key
                        if issue_key in issue_open_monthyear:
                            item['issue_count'] = issue_open_monthyear[issue_key]
                        else:
                            item['issue_count'] = 0
                        if issue_key in issue_close_monthyear:
                            item['close_issue_count'] = issue_close_monthyear[issue_key]
                        else:
                            item['close_issue_count'] = 0
                        OsslibStatisticIssueYearmonth(**item)
                
                #统计commit hourday
                day_week = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
                if oss_commit_hourday.count() > 0:
                    for per_oss_commit_hourday in oss_commit_hourday:
                        day = per_oss_commit_hourday.weekday_hour[:3]
                        day_index = day_week.index(day)
                        hour = int(per_oss_commit_hourday.weekday_hour[4:])
                        osslibstatisticyearmonth = OsslibStatisticCommitHourday.select(
                            AND(OsslibStatisticCommitHourday.q.community_id == community_id,
                                OsslibStatisticCommitHourday.q.day == day_index,
                                OsslibStatisticCommitHourday.q.hour == hour))
                        if osslibstatisticyearmonth.count() > 0:
                            for per_osslibstatisticyearmonth in osslibstatisticyearmonth:
                                per_osslibstatisticyearmonth.commit_count = int(per_osslibstatisticyearmonth.commit_count) + int(per_oss_commit_hourday.commits)
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['day'] = int(day_index)
                            item['hour'] = int(hour)
                            item['commit_count'] = int(per_oss_commit_hourday.commits)
                            OsslibStatisticCommitHourday(**item)
                # 统计pull
                
                for pull_key in pull_monthyear:
                    osslibstatisticyearmonth = OsslibStatisticPullYearmonth.select(
                        AND(OsslibStatisticPullYearmonth.q.community_id == community_id,
                            OsslibStatisticPullYearmonth.q.yearmonth == pull_key))
                    if osslibstatisticyearmonth.count() > 0:
                        for per_osslibstatisticyearmonth in osslibstatisticyearmonth:
                            if pull_key in pull_open_monthyear:
                                per_osslibstatisticyearmonth.pull_count = per_osslibstatisticyearmonth.pull_count + \
                                                                           pull_open_monthyear[pull_key]
                            if pull_key in pull_merged_monthyear:
                                per_osslibstatisticyearmonth.merged_pull_count = per_osslibstatisticyearmonth.merged_pull_count + \
                                                                                 pull_merged_monthyear[pull_key]
                    else:
                        item = dict()
                        item['community_id'] = community_id
                        item['yearmonth'] = pull_key
                        if pull_key in pull_open_monthyear:
                            item['pull_count'] = pull_open_monthyear[pull_key]
                        else:
                            item['pull_count'] = 0
                        if pull_key in pull_merged_monthyear:
                            item['merged_pull_count'] = pull_merged_monthyear[pull_key]
                        else:
                            item['merged_pull_count'] = 0
                        OsslibStatisticPullYearmonth(**item)
                if oss_commit.count() > 0:
                    for per_oss_commit in oss_commit:
                        osslibstatisticyearmonth = OsslibStatisticCommitYearmonth.select(AND(OsslibStatisticCommitYearmonth.q.community_id==community_id,
                                                                          OsslibStatisticCommitYearmonth.q.yearmonth==per_oss_commit.yearmonth))
                        if osslibstatisticyearmonth.count() > 0:
                            for per_osslibstatisticyearmonth in osslibstatisticyearmonth:
                                per_osslibstatisticyearmonth.commits_count = per_osslibstatisticyearmonth.commits_count + per_oss_commit.commits
                        else:
                            item = dict()
                            item['community_id'] = community_id
                            item['yearmonth'] = per_oss_commit.yearmonth
                            item['commits_count'] = per_oss_commit.commits
                            OsslibStatisticCommitYearmonth(**item)
            
                osslib_statistic_info = OsslibStatistic.get(statistic_id)
                osslib_statistic_info.loc = osslib_statistic_info.loc + loc
                osslib_statistic_info.doc = osslib_statistic_info.doc + doc
                osslib_statistic_info.coc = osslib_statistic_info.coc + coc
                osslib_statistic_info.foc = osslib_statistic_info.foc + foc
                osslib_statistic_info.issue_comment_count = osslib_statistic_info.issue_comment_count + issue_comment_count
                osslib_statistic_info.core_issue_count = osslib_statistic_info.core_issue_count + core_issue_count
                osslib_statistic_info.issue_close_time = osslib_statistic_info.issue_close_time + issue_close_time/3600/24
                osslib_statistic_info.issue_count = osslib_statistic_info.issue_count + issue_count
                osslib_statistic_info.issue_close_count = osslib_statistic_info.issue_close_count + issue_close_count
                osslib_statistic_info.pull_count = osslib_statistic_info.pull_count + pull_count
                osslib_statistic_info.pull_merged_count = osslib_statistic_info.pull_merged_count + pull_merged_count
                osslib_statistic_info.pull_merged_time = osslib_statistic_info.pull_merged_time + pull_merged_time/3600/24
                osslib_statistic_info.pull_comment_count = osslib_statistic_info.pull_comment_count + pull_comment_count
                osslib_statistic_info.pull_review_count = osslib_statistic_info.pull_review_count + pull_review_count
                osslib_statistic_info.pull_review_comment_count = osslib_statistic_info.pull_review_comment_count + pull_review_comment_count
                osslib_statistic_info.core_pull_count = osslib_statistic_info.core_pull_count + core_pull_count
                osslib_statistic_info.core_developer_count = osslib_statistic_info.core_developer_count + core_developer_count
                osslib_statistic_info.fork_count = osslib_statistic_info.fork_count + fork_count
                osslib_statistic_info.star_count = osslib_statistic_info.star_count + star_count
                osslib_statistic_info.all_days = osslib_statistic_info.all_days + all_day
                osslib_statistic_info.active_days = osslib_statistic_info.active_days + active_day
                
                lock.release()

            except BaseException as ex:
                print(ex)
    '''





