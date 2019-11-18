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


# 数据统计
class Statistics:

    def __init__(self):
        manager = get_thread_task_queue('statistics_queue')
        manager2 = get_thread_task_dict('statistics_dict')
        self.task_queue = manager.statistics_queue()
        self.task_dict = manager2.statistics_dict()

    def oss_stat(self):
        community_info = OsslibCommunity.select()
        data_dict = dict()
        data_dict.__setitem__('loc', 0)
        data_dict.__setitem__('doc', 0)
        data_dict.__setitem__('coc', 0)
        data_dict.__setitem__('foc', 0)
        #'''数据可视化 可删 2019.10.29 js
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

        lock = multiprocessing.Lock()
        for per_community_info in community_info:
            community_id = per_community_info.id
            community_list_info = OsslibCommunityList.select(OsslibCommunityList.q.community_id == community_id)
            item = dict()
            item['community_id'] = community_id
            item['update_time'] = time.strftime('%Y-%m-%d')
            return_info = OsslibStatistic(**item)
            #exit(0)
            #osslib_statistic = OsslibStatistic.select(OsslibStatistic.q.community_id == community_id)
            #self.task_dict.update({str(community_id):osslib_statistic[0]})
            #self.task_dict.update({str(community_id):data_dict})
            #print(global_dict)
            for per_community_list in community_list_info:
                trans_info = []
                trans_info.append(per_community_list.meta_id)
                trans_info.append(per_community_list.community_id)
                trans_info.append(return_info.id)
                self.task_queue.put(trans_info)
        for i in range(4):
            p = multiprocessing.Process(target=self._statistic, args=(self.task_queue, i, lock))
            p.start()
        p.join()
        print('over')

    @staticmethod
    def _statistic(q, i, lock):
        while True:
            if q.empty():
                break
            try:
                info = q.get()
                mata_id = info[0]
                community_id = info[1]
                statistic_id = info[2]
                oss_mata = OsslibMetadata_2.get(mata_id)
                loc = oss_mata.oss_line_count
                doc = oss_mata.oss_developer_count
                foc = oss_mata.oss_file_count
                coc = oss_mata.oss_commit_count
                star_count = oss_mata.oss_star
                fork_count = oss_mata.oss_fork
                all_day = oss_mata.oss_all_day
                active_day = oss_mata.oss_active_day

                #oss_commit = OsslibActivityYearMonth.select(OsslibActivityYearMonth.q.oss_id == oss_mata.oss_id)
                #oss_issue = OsslibIssue.select(OsslibIssue.q.oss_id == oss_mata.oss_id)
                #oss_pull = OsslibPulls.select(OsslibPulls.q.oss_id == oss_mata.oss_id)
                #oss_commit_hourday = OsslibActivityHourOfWeek.select(OsslibActivityHourOfWeek.q.oss_id == oss_mata.oss_id)
                #oss_developer = OsslibAuthorMonth.select(OsslibAuthorMonth.q.oss_id == oss_mata.oss_id)
                oss_issue_comment =OsslibIssueComment.select(OsslibIssueComment.q.oss_id == oss_mata.oss_id)
                '''
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
                '''
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


                '''
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
                '''

                '''
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
                '''
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
                '''
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
                '''
                '''
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
                        '''
                '''
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
                    '''
                lock.release()

            except BaseException as ex:
                print(ex)








