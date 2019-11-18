import scrapy
import json
import requests
from MOOSE_spider.items import *
from MOOSE_spider.spiders.request_header import *
import time
import re
import random
import pymysql
import emoji
from MOOSE_spider import settings
from bs4 import BeautifulSoup
import re
import base64

emoji_pattern = re.compile(u"(\ud83d[\ude00-\ude4f])|"
                           # emoticons 
                           u"(\ud83c[\udf00-\uffff])|"
                           # symbols & pictographs (1 of 2) 
                           u"(\ud83d[\u0000-\uddff])|"
                           # symbols & pictographs (2 of 2) 
                           u"(\ud83d[\ude80-\udeff])|"
                           # transport & map symbols 
                           u"(\ud83c[\udde0-\uddff])"
                           # flags (iOS) 
                           "+", flags=re.UNICODE)


def remove_emoji(text):
    return emoji_pattern.sub(r'', text)


def dbHandle():
    conn = pymysql.connect(
        host=settings.MYSQL_HOST,
        db=settings.MYSQL_DBNAME,
        user=settings.MYSQL_USER,
        passwd=settings.MYSQL_PASSWD,
        charset='utf8',
        use_unicode=True
    )
    return conn

class OsslibSpider(scrapy.Spider):
    name = "MOOSE"
    def __init__(self, repo=None, *args, **kwargs):
        super(OsslibSpider, self).__init__(*args, **kwargs)

    scrapyed_list = []
    dbObject = dbHandle()
    cursor = dbObject.cursor()
    # get repo from monitor list
    cursor.execute("select repo_full_name from github_repo_base")
    results = cursor.fetchall()
    for result in results:
        scrapyed_list.append("https://api.github.com/repos/" + result[0])
    repo_index = 0
    start_urls = ['https://api.github.com/repos/ThunderCls/xAnalyzer']

    def parse(self, response):
        try:
            repos_data = json.loads(response.body.decode('utf-8'))
            repo_url = repos_data['url']
            oss_id = repos_data['id']

            # repo base information
            try:
                oss_star = repos_data['stargazers_count']
            except BaseException as e:
                oss_star = 0
            try:
                oss_fork = repos_data['forks']
            except BaseException as e:
                oss_fork = 0
            try:
                oss_subscriber = repos_data['subscribers_count']
            except BaseException as e:
                oss_subscriber = 0
            oss_fullname = repos_data['full_name']
            oss_name = repos_data['name']
            oss_description = repos_data['description']
            try:
                oss_create_time = repos_data['created_at']
            except BaseException as ex:
                oss_create_time = ''
            try:
                oss_owner_id = int(repos_data['owner']['id'])
            except BaseException as ex:
                oss_owner_id = 0
            try:
                oss_owner_type = repos_data['owner']['type']
            except BaseException as ex:
                oss_owner_type = ''
            try:
                oss_size = int(repos_data['size'])
            except BaseException as ex:
                oss_size = 0
            try:
                oss_main_language = repos_data['language']
            except BaseException as ex:
                oss_main_language = ''
            try:
                oss_homepage = repos_data['homepage']
            except BaseException as ex:
                oss_homepage = ''
            if oss_homepage != '' or oss_homepage is not None:
                has_page = 1
            else:
                has_page = 0
            try:
                oss_license = repos_data['license']['name']
            except BaseException as e:
                oss_license = ''
            try:
                oss_git_url = repos_data['clone_url']
                oss_git_tool = 'Git'
            except BaseException as e:
                oss_git_url = ''
                oss_git_tool = ''
            try:
                has_wiki = int(repos_data['has_wiki'])
            except BaseException as ex:
                has_wiki = 0
            last_update_date = repos_data['updated_at']
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            readmeinfo = get_html_json(repos_data['url'] + "/readme", getHeader())[0]
            if len(readmeinfo) > 0:
                try:
                    readme = readmeinfo['content']
                    readme = str(base64.b64decode(readme), encoding="utf-8").replace('\r', '').replace('\n', '')
                except:
                    readme = ''
            try:
                # language
                languages_count = 0
                languages_url = repos_data['languages_url']
                languages_info = requests.get(languages_url, headers=getHeader()).text
                languages_data = json.loads(languages_info)
                languages = {}
                if isinstance(languages_data, dict):  # 判断是否是字典类型isinstance 返回True false
                    for key in languages_data:
                        languages[key] = languages_data[key]
                        languages_count += 1
                languages = json.dumps(languages)

            except BaseException as e:
                languages = ''
            try:
                metadata = MooseMetadata()
                metadata['oss_language'] = languages
                metadata['oss_star'] = oss_star
                metadata['oss_repo_url'] = repo_url
                metadata['oss_fork'] = oss_fork
                metadata['oss_subscriber'] = oss_subscriber
                metadata['oss_id'] = oss_id
                metadata['oss_fullname'] = oss_fullname
                metadata['oss_name'] = oss_name
                metadata['oss_description'] = oss_description
                metadata['oss_create_time'] = oss_create_time
                metadata['oss_owner_id'] = oss_owner_id
                metadata['oss_owner_type'] = oss_owner_type
                metadata['oss_size'] = oss_size
                metadata['oss_main_language'] = oss_main_language
                metadata['oss_language_count'] = languages_count
                metadata['oss_homepage'] = oss_homepage
                metadata['oss_license'] = oss_license
                metadata['oss_git_url'] = oss_git_url
                metadata['oss_git_tool'] = oss_git_tool
                metadata['has_wiki'] = has_wiki
                metadata['has_pages'] = has_page
                metadata['oss_lastupdate_time'] = last_update_date
                metadata['update_time'] = update_time
                metadata['readme'] = readme

            except BaseException as e:
                metadata['oss_language'] = ''
                metadata['oss_id'] = oss_id
                metadata['oss_star'] = 0
                metadata['oss_fork'] = 0
                metadata['oss_subscriber'] = 0
            yield metadata

            # developer数据采集
            #contributors_url = repos_data['contributors_url'] + "?per_page=100"
            #yield scrapy.Request(contributors_url, meta={"oss_id": oss_id}, callback=self.detail_contributors_parse, headers=getHeader())

            #commit data crawl
            commit_url = repos_data['commits_url'][0:-6]+"?per_page=100"
            yield scrapy.Request(commit_url, meta={"oss_id": oss_id}, callback=self.detail_commit_parse, headers=getHeader())

            #pulls data crawl
            pulls_url = repos_data["pulls_url"][0:-9] + "?state=all&sort=updated&direction=asc&per_page=100"
            yield scrapy.Request(pulls_url, meta={"oss_id": oss_id, "pull_url": repos_data["pulls_url"][0:-9]}, callback=self.detail_pulls_parse, headers=getHeader())

            #commit comment data crawl
            commit_comment_url = repos_data["comments_url"][0:-9] + "?sort=updated&direction=asc&per_page=100"
            yield scrapy.Request(commit_comment_url, meta={"oss_id": oss_id, "commit_comment_url": repos_data["comments_url"][0:-9]}, callback=self.detail_commit_comment_parse, headers=getHeader())

            # issues data crawl
            issues_url = repos_data["issues_url"][0:-9] + "?state=all&sort=updated&direction=asc&per_page=100"
            yield scrapy.Request(issues_url, meta={"oss_id": oss_id}, callback=self.detail_issues_parse, headers=getHeader())

            # topic data crawl
            topics_response = requests.get(url=repos_data['url']  + "/topics", headers=getHeader())
            topics_text = topics_response.text
            topic_jsonobj = json.loads(topics_text)
            topic_items = dict()
            try:
                for topic_name in topic_jsonobj['names']:
                    topic_items['oss_id'] = int(oss_id)
                    topic_items['topic'] = topic_name
                    yield topic_items
            except BaseException as ex:
                print(ex)
        except BaseException as e:
            print(258)
            print(e)
        self.repo_index = self.repo_index + 1
        yield scrapy.Request(self.scrapyed_list[self.repo_index], callback=self.parse, headers=getHeader())


    def detail_issues_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        issue_open_monthyear = dict()
        issue_close_monthyear = dict()
        issue_monthyear = []
        # Query current issue statistics
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("select issue_count,issue_close_count,issue_close_time, core_issue_count,issue_comment_count from MOOSE_statistic where oss_id=%s",(oss_id))
        result = cursor.fetchone()
        cursor.close()
        issue_last_at = ''
        if result:
            issue_count = int(result[0]) if result[0] is not None else 0
            issue_close_count = int(result[1]) if result[1] is not None else 0
            issue_close_time = int(result[2]) if result[2] is not None else 0
            core_issue_count = int(result[3]) if result[3] is not None else 0
            issue_comment_count = int(result[4]) if result[4] is not None else 0
        else:
            issue_count = 0
            issue_close_count = 0
            issue_close_time = 0
            core_issue_count = 0
            issue_comment_count = 0
        index = 0
        for repos_per_data in repos_data:
            index += 1

            if "pull_request" in repos_per_data:
                continue
            issue_count += 1
            #按年度月份统计 issue数量
            open_at_month = repos_per_data['created_at'][:7]
            # 判断是否是最后一个元素，是的话，记录一下时间
            if index == len(repos_data):
                issue_last_at = repos_per_data['updated_at']
            if open_at_month in issue_open_monthyear.keys():
                issue_open_monthyear[open_at_month] += 1
            else:
                issue_open_monthyear[open_at_month] = 1
            if open_at_month not in issue_monthyear:
                issue_monthyear.append(open_at_month)

            #统计issue close 数量
            if repos_per_data['state'] == 'closed':
                issue_close_count += 1
                issue_create_at = repos_per_data['created_at']
                issue_close_at = repos_per_data['closed_at']
                issue_close_time += (time.mktime(time.strptime(issue_close_at, "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(time.strptime(issue_create_at, "%Y-%m-%dT%H:%M:%SZ")))/3600/24
                close_at_month = issue_close_at[:7]
                if close_at_month in issue_close_monthyear.keys():
                    issue_close_monthyear[close_at_month] += 1
                else:
                    issue_close_monthyear[close_at_month] = 1
                if close_at_month not in issue_monthyear:
                    issue_monthyear.append(close_at_month)

            issue_comment_count += repos_per_data['comments']
            issue_user_type = repos_per_data['author_association']
            if issue_user_type == 'MEMBER' or issue_user_type == 'COLLABORATOR':
                core_issue_count += 1

            #统计用户
            '''
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.detail_owner_parse, headers=getHeader())
            '''
        Issues_Info_statistics = MOOSEStatisticsIssue()
        Issues_Info_statistics['oss_id'] = oss_id
        Issues_Info_statistics['issue_count'] = issue_count
        Issues_Info_statistics['issue_close_count'] = issue_close_count
        Issues_Info_statistics['issue_comment_count'] = issue_comment_count
        Issues_Info_statistics['issue_close_time'] = issue_close_time
        Issues_Info_statistics['core_issue_count'] = core_issue_count
        yield Issues_Info_statistics

        #按年度月份统计 issue数量
        for issue_key in issue_monthyear:
            Issues_Yearmonth_statistics = MOOSEStatisticsIssueMonth()
            Issues_Yearmonth_statistics['yearmonth'] = issue_key
            Issues_Yearmonth_statistics['oss_id'] = oss_id
            if issue_key in issue_open_monthyear:
                Issues_Yearmonth_statistics['issue_count'] = issue_open_monthyear[issue_key]
            else:
                Issues_Yearmonth_statistics['issue_count'] = 0
            if issue_key in issue_close_monthyear:
                Issues_Yearmonth_statistics['close_issue_count'] = issue_close_monthyear[issue_key]
            else:
                Issues_Yearmonth_statistics['close_issue_count'] = 0
            yield Issues_Yearmonth_statistics

        try:
            dbObject = dbHandle()
            cursor = dbObject.cursor()
            cursor.execute("update  MOOSE_metadata set issue_at=%s where oss_id=%s ", (issue_last_at, oss_id))
            cursor.connection.commit()
            cursor.close()
        except BaseException as ex:
            print(258)
            print(ex)
            dbObject.rollback()
        listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
        if (len(listLink_next_url) > 0):
            yield scrapy.Request(listLink_next_url[0], meta={"oss_id": oss_id},
                                 callback=self.detail_issues_parse,
                                 headers=getHeader())

    def detail_pulls_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        pull_url = response.meta['pull_url']
        pull_open_monthyear = dict()
        pull_merged_monthyear = dict()
        pull_monthyear = []
        # 查询当前的pull统计数据
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        try:
            cursor.execute("select pull_count, pull_merged_count, pull_comment_count, pull_review_count,core_pull_count, "
                       "pull_merged_time, pull_review_comment_count,core_review_comment_count,core_review_count from MOOSE_statistic where oss_id=%s",(oss_id))
            result = cursor.fetchone()
            cursor.close()
        except BaseException as ex:
            print(397)
        pull_last_at = ''
        if result:
            pull_count = int(result[0]) if result[0] is not None else 0
            pull_merged_count = int(result[1]) if result[1] is not None else 0
            pull_comment_count = int(result[2]) if result[2] is not None else 0
            pull_review_count = int(result[3]) if result[3] is not None else 0
            core_pull_count = int(result[4]) if result[4] is not None else 0
            pull_merged_time = int(result[5]) if result[5] is not None else 0
            pull_review_comment_count = int(result[6]) if result[6] is not None else 0
            core_review_comment_count = int(result[7]) if result[7] is not None else 0
            core_review_count = int(result[8]) if result[8] is not None else 0
        else:
            pull_count = 0
            pull_merged_count = 0
            pull_comment_count = 0
            pull_review_count = 0
            core_pull_count = 0
            pull_merged_time = 0
            pull_review_comment_count = 0
            core_review_comment_count = 0
            core_review_count = 0
        index = 0
        for repos_per_data in repos_data:
            #####################
            Pulls_Info_item = MOOSEPulls()
            Pulls_Info_item['oss_id'] = oss_id
            Pulls_Info_item['pull_id'] = repos_per_data['id']
            pull_id = repos_per_data['id']
            Pulls_Info_item['pull_number'] = repos_per_data['number']
            pull_no = repos_per_data['number']
            if (repos_per_data['state'] == 'open'):
                Pulls_Info_item['pull_state'] = 0
            elif (repos_per_data['state'] == 'closed'):
                Pulls_Info_item['pull_state'] = 1
            else:
                Pulls_Info_item['pull_state'] = 2
            Pulls_Info_item['pull_created_at'] = repos_per_data['created_at']
            Pulls_Info_item['pull_update_at'] = repos_per_data['updated_at']
            Pulls_Info_item['pull_closed_at'] = repos_per_data['closed_at']
            Pulls_Info_item['pull_merged_at'] = repos_per_data['merged_at']
            if (repos_per_data['merged_at'] == None):
                Pulls_Info_item['pull_is_merged'] = 0
            else:
                Pulls_Info_item['pull_is_merged'] = 1
            Pulls_Info_item['pull_author_association'] = repos_per_data['author_association']
            Pulls_Info_item['user_id'] = repos_per_data['user']['id']
            Pulls_Info_item['pull_body'] = repos_per_data['body']
            Pulls_Info_item['pull_title'] = repos_per_data['title']

            Pulls_Info_item['update_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            Pulls_Info_item['request_reviewer'] = ''
            pull_request_reviewer = []
            if len(repos_per_data['requested_reviewers']) > 0:
                for reviewer in repos_per_data['requested_reviewers']:
                    Pulls_Info_item['request_reviewer'] += str(reviewer['id']) + "|"
                    pull_request_reviewer.append(reviewer['id'])

            #####################
            index += 1
            pull_no = repos_per_data['number']
            pull_count += 1
            # 按年度月份统计 pull数量
            open_at_month = repos_per_data['created_at'][:7]
            # 判断是否是最后一个元素，是的话，记录一下时间
            if index == len(repos_data):
                pull_last_at = repos_per_data['updated_at']
            if open_at_month in pull_open_monthyear.keys():
                pull_open_monthyear[open_at_month] += 1
            else:
                pull_open_monthyear[open_at_month] = 1
            if open_at_month not in pull_monthyear:
                pull_monthyear.append(open_at_month)

            # 统计pull merged 数量
            if (repos_per_data['merged_at'] != None):
                pull_merged_count += 1
                pull_create_at = repos_per_data['created_at']
                pull_merged_at = repos_per_data['merged_at']
                pull_merged_time += (time.mktime(time.strptime(pull_merged_at, "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(time.strptime(pull_create_at, "%Y-%m-%dT%H:%M:%SZ"))) / 3600 / 24
                merged_at_month = pull_merged_at[:7]
                if merged_at_month in pull_merged_monthyear.keys():
                    pull_merged_monthyear[merged_at_month] += 1
                else:
                    pull_merged_monthyear[merged_at_month] = 1
                if merged_at_month not in pull_monthyear:
                    pull_monthyear.append(merged_at_month)
            pull_user_type = repos_per_data['author_association']
            #统计核心开发人员
            if pull_user_type == 'MEMBER' or pull_user_type == 'COLLABORATOR':
                core_pull_count += 1
                core_user_Info_statistics = MOOSEStatisticsUserRepo()
                core_user_Info_statistics['oss_id'] = oss_id
                core_user_Info_statistics['user_id'] = repos_per_data['user']['id']
                yield core_user_Info_statistics

            #进入详情页，计算comment数量和review comment数量
            pull_detail_url = pull_url + "/" + str(pull_no)
            pull_detail_html = requests.get(pull_detail_url, headers=getHeader()).text
            pull_datail_html_info = json.loads(pull_detail_html)
            if (pull_datail_html_info and len(pull_datail_html_info) > 0 and "message" not in pull_datail_html_info):
                pull_comment_count += pull_datail_html_info['comments']
                pull_review_comment_count += pull_datail_html_info['review_comments']
                Pulls_Info_item['pull_comments'] = pull_datail_html_info['comments']
                Pulls_Info_item['review_comments'] = pull_datail_html_info['review_comments']
            else:
                Pulls_Info_item['pull_comments'] = 0
                Pulls_Info_item['review_comments'] = 0


            # 查询review
            pull_review_url = pull_url + "/" + str(pull_no) + "/reviews"
            pull_review_html = requests.get(pull_review_url, headers=getHeader()).text
            pull_review_html_info = json.loads(pull_review_html)
            if (pull_review_html_info and len(pull_review_html_info) > 0 and "message" not in pull_review_html_info):
                Pulls_Info_item['pull_is_reviewed'] = 1
                pull_review_count += 1
                for review in pull_review_html_info:
                    review_user_type = review['author_association']
                    if review_user_type == 'MEMBER' or review_user_type == 'COLLABORATOR':
                        core_review_count += 1
            else:
                Pulls_Info_item['pull_is_reviewed'] = 0
            #查询review comment
            if pull_datail_html_info['review_comments'] != 0:
                pull_review_comment_url = pull_url + "/" + str(pull_no) + "/comments"
                pull_review_comment_html = requests.get(pull_review_comment_url, headers=getHeader()).text
                pull_review_comment_html_info = json.loads(pull_review_comment_html)
                if (pull_review_comment_html_info and len(pull_review_comment_html_info) > 0 and "message" not in pull_review_comment_html_info):
                    for review_comment in pull_review_comment_html_info:
                        review_comment_user_type = review_comment['author_association']
                        if review_comment_user_type == 'MEMBER' or review_comment_user_type == 'COLLABORATOR':
                            core_review_comment_count += 1
            yield Pulls_Info_item
            # 统计用户
            '''
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.detail_owner_parse, headers=getHeader())
            '''
        Pull_Info_statistics = MOOSEStatisticsPull()
        Pull_Info_statistics['oss_id'] = oss_id
        Pull_Info_statistics['pull_count'] = pull_count
        Pull_Info_statistics['pull_merged_count'] = pull_merged_count
        Pull_Info_statistics['pull_merged_time'] = pull_merged_time
        Pull_Info_statistics['pull_comment_count'] = pull_comment_count
        Pull_Info_statistics['pull_review_count'] = pull_review_count
        Pull_Info_statistics['core_pull_count'] = core_pull_count
        Pull_Info_statistics['pull_review_comment_count'] = pull_review_comment_count
        Pull_Info_statistics['core_review_comment_count'] = core_review_comment_count
        Pull_Info_statistics['core_review_count'] = core_review_count

        yield Pull_Info_statistics

        # 按年度月份统计 issue数量
        for pull_key in pull_monthyear:
            Pull_Yearmonth_statistics = MOOSEStatisticsPullMonth()
            Pull_Yearmonth_statistics['yearmonth'] = pull_key
            Pull_Yearmonth_statistics['oss_id'] = oss_id
            if pull_key in pull_open_monthyear:
                Pull_Yearmonth_statistics['pull_count'] = pull_open_monthyear[pull_key]
            else:
                Pull_Yearmonth_statistics['pull_count'] = 0
            if pull_key in pull_merged_monthyear:
                Pull_Yearmonth_statistics['merged_pull_count'] = pull_merged_monthyear[pull_key]
            else:
                Pull_Yearmonth_statistics['merged_pull_count'] = 0
            yield Pull_Yearmonth_statistics
        try:
            dbObject = dbHandle()
            cursor = dbObject.cursor()
            cursor.execute("update  MOOSE_metadata set pull_at=%s where oss_id=%s ", (pull_last_at, oss_id))
            cursor.connection.commit()
            cursor.close()
        except BaseException as ex:
            print(526)
            print(ex)
            dbObject.rollback()

        listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
        if (len(listLink_next_url) > 0):
            yield scrapy.Request(listLink_next_url[0], meta={"oss_id": oss_id, "pull_url": pull_url},
                                 callback=self.detail_pulls_parse,
                                 headers=getHeader())

    def detail_commit_comment_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        commit_comment_url = response.meta['commit_comment_url']

        # 查询当前的commit comment统计数据
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        try:
            cursor.execute("select commit_comment_count, core_commit_comment_count from MOOSE_statistic where oss_id=%s",(oss_id))
            result = cursor.fetchone()
            cursor.close()
        except BaseException as ex:
            print(553)
        commit_comment_last_at = ''
        if result:
            commit_comment_count = int(result[0]) if result[0] is not None else 0
            core_commit_comment_count = int(result[1]) if result[1] is not None else 0
        else:
            commit_comment_count = 0
            core_commit_comment_count = 0
        index = 0
        for repos_per_data in repos_data:
            index += 1
            commit_comment_count += 1
            if index == len(repos_data):
                commit_comment_last_at = repos_per_data['updated_at']
            commit_comment_user_type = repos_per_data['author_association']
            if commit_comment_user_type == 'MEMBER' or commit_comment_user_type == 'COLLABORATOR':
                core_commit_comment_count += 1

        commit_comment_Info_statistics = MOOSEStatisticsComment()
        commit_comment_Info_statistics["oss_id"] = oss_id
        commit_comment_Info_statistics["core_commit_comment_count"] = core_commit_comment_count
        commit_comment_Info_statistics["commit_comment_count"] = commit_comment_count
        yield commit_comment_Info_statistics
        try:
            dbObject = dbHandle()
            cursor = dbObject.cursor()
            cursor.execute("update  MOOSE_metadata set commit_comment_at=%s where oss_id=%s ", (commit_comment_last_at, oss_id))
            cursor.connection.commit()
            cursor.close()
        except BaseException as ex:
            dbObject.rollback()
        listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
        if (len(listLink_next_url) > 0):
            yield scrapy.Request(listLink_next_url[0], meta={"oss_id": oss_id, "commit_comment_url": commit_comment_url}, callback=self.detail_commit_comment_parse,
                                 headers=getHeader())

    def detail_commit_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        commit_monthyear = dict()

        #查询当前的commit统计数据
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("select commit_count from MOOSE_statistic where oss_id=%s",(oss_id))
        result = cursor.fetchone()
        cursor.close()
        if result:
            commit_count = int(result[0]) if result[0] is not None else 0
        else:
            commit_count = 0
        index = 0
        for repos_per_data in repos_data:
            index += 1
            commit_count += 1
            #按年度月份统计 issue数量
            commit_month = repos_per_data['commit']['committer']['date'][:7]
            # 判断是否是最后一个元素，是的话，记录一下时间
            if commit_month in commit_monthyear.keys():
                commit_monthyear[commit_month] += 1
            else:
                commit_monthyear[commit_month] = 1

            #统计用户
            '''
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.detail_owner_parse, headers=getHeader())
            '''
        Commit_Info_statistics = MOOSEStatisticsCommit()
        Commit_Info_statistics['oss_id'] = oss_id
        Commit_Info_statistics['commit_count'] = commit_count
        yield Commit_Info_statistics

        #按年度月份统计 issue数量
        for commit_key in commit_monthyear:
            commit_Yearmonth_statistics = MOOSEStatisticsCommitMonth()
            commit_Yearmonth_statistics['yearmonth'] = commit_key
            commit_Yearmonth_statistics['oss_id'] = oss_id
            commit_Yearmonth_statistics['commit_count'] = commit_monthyear[commit_key]
            yield commit_Yearmonth_statistics
        listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
        if (len(listLink_next_url) > 0):
            yield scrapy.Request(listLink_next_url[0], meta={"oss_id": oss_id},
                                 callback=self.detail_commit_parse,
                                 headers=getHeader())

    def topic_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        oss_id = response.meta['oss_id']
        topic_items = MOOSEStatisticsTopic
        for topic_name in repos_data['names']:
            topic_items['oss_id'] = oss_id
            topic_items['topic'] = topic_name
            yield topic_items

    def detail_owner_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        User_Info_item = MOOSEUser()
        User_Info_item['user_id'] = repos_data['id']
        User_Info_item['user_name'] = repos_data['login']
        if repos_data['name']!=None:
            User_Info_item['user_fullname'] = repos_data['name']
        else:
            User_Info_item['user_fullname'] = repos_data['login']
        User_Info_item['avatar_url'] = repos_data['avatar_url']
        try:
            User_Info_item['follows_count'] = repos_data['followers']
        except BaseException as e:
            User_Info_item['follows_count'] = 0
        User_Info_item['repos_count'] = repos_data['public_repos']
        User_Info_item['blog_url'] = str(repos_data['blog'])
        User_Info_item['location'] = str(repos_data['location'])
        User_Info_item['email_url'] = str(repos_data['email'])
        User_Info_item['company'] = str(repos_data['company'])
        User_Info_item['org_member_count'] = 0
        User_Info_item['user_type'] = repos_data['type']
        User_Info_item['user_create_time'] = repos_data['created_at']
        User_Info_item['update_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        User_Info_item['user_update_time'] = repos_data['updated_at']
        yield User_Info_item

    def is_user_exit(self, uid):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("select * from MOOSE_user where user_id=%s", (uid))
        result = cursor.fetchone()
        if result:
            return 1
        else:
            return 0


