import scrapy
import json
import requests
from MOOSE_time.items import *

from influxdb import InfluxDBClient
import time
import re
import random
import pymysql
import emoji
from MOOSE_time import settings
from MOOSE_time.spiders.request_header import *
from bs4 import BeautifulSoup
import re
import base64

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

class MOOSE_TIMESpider(scrapy.Spider):
    name = "MOOSE"

    def __init__(self, repo=None, *args, **kwargs):
        super(MOOSE_TIMESpider, self).__init__(*args, **kwargs)
    client = InfluxDBClient('192.168.3.11', 8086, 'moose', 'moose', 'moose')
    #client.query("drop measurement moose_index")
    #exit(0)
    #result = client.query("select sum(index_count) from moose_index where  time <'2019-12"
    #                      "-29T00:00:00Z' and  community_id='15' group by time(24h) fill(0);").get_points()
    result = client.query("select * from moose_pull where community_id='15' order by time desc;").get_points()
    print("Result: {0}".format(result))
    for aa in result:
        print(aa)

    #exit(0)
    scrapyed_list = []
    oss_event_id = dict()
    community_id = dict()
    dbObject = dbHandle()
    cursor = dbObject.cursor()
    # get repo from monitor list and get last event/issue/pr/commit  id
    cursor.execute("select oss_name, oss_id, community_id from moose_community_list")
    results = cursor.fetchall()
    for result in results:
        oss_id = result[1]
        oss_event_id.update({oss_id:[]})
        scrapyed_list.append("https://api.github.com/repos/" + result[0])
        cursor.execute("select event_id, issue_id, pullrequest_id, commit_time, comment_id, issue_comment_id from moose_event_id where oss_id='" + str(oss_id) + "'")
        last_oss_event_id = cursor.fetchone()
        if last_oss_event_id != None and len(last_oss_event_id)>0:
            for per_last_id in last_oss_event_id:
                if per_last_id is None or per_last_id=='':
                    per_last_id = 0
                oss_event_id[oss_id].append(per_last_id)
        else:
            cursor.execute("insert into  moose_event_id  (oss_id) values ('" + str( oss_id) + "')")
            dbObject.commit()
            for i in range(4):
                oss_event_id[oss_id].append(0)
        community_id[result[1]] = result[2]
    print(oss_event_id)
    repo_index = 0
    start_urls = [scrapyed_list[0]]

    def parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        oss_id = repos_data['id']

        # issues data crawl
        issues_url = repos_data["issues_url"][0:-9] + "?state=all&sort=created&direction=desc&per_page=100"
        yield scrapy.Request(issues_url, meta={"oss_id": oss_id}, callback=self.parse_issue, headers=getHeader())

        # issues comment data crawl
        issues_comment_url = repos_data["issue_comment_url"][0:-9] + "?sort=created&direction=desc&per_page=100"
        yield scrapy.Request(issues_comment_url, meta={"oss_id": oss_id}, callback=self.parse_issue_comment, headers=getHeader())

        # pulls data crawl
        pulls_url = repos_data["pulls_url"][0:-9] + "?state=all&sort=created&direction=desc&per_page=100"
        yield scrapy.Request(pulls_url, meta={"oss_id": oss_id, "pull_url": repos_data["pulls_url"][0:-9]}, callback=self.parse_pullrequest, headers=getHeader())

        # commit data crawl
        commit_url = repos_data['commits_url'][0:-6] + "?sort=created&direction=desc&per_page=100&per_page=100"
        yield scrapy.Request(commit_url, meta={"oss_id": oss_id}, callback=self.parse_commit, headers=getHeader())

        # commit comment data crawl
        commit_comment_url = repos_data["comments_url"][0:-9] + "?sort=created&direction=desc&per_page=100"
        yield scrapy.Request(commit_comment_url, meta={"oss_id": oss_id, "commit_comment_url": repos_data["comments_url"][0:-9]}, callback=self.parse_commit_comment, headers=getHeader())

        # index data crawl
        event_url = repos_data["events_url"]
        yield scrapy.Request(event_url, meta={"oss_id": oss_id}, callback=self.parse_event, headers=getHeader())

        self.repo_index = self.repo_index + 1
        if self.repo_index <= len(self.scrapyed_list) - 1:
            yield scrapy.Request(self.scrapyed_list[self.repo_index], meta={"is_first": 1}, callback=self.parse, headers=getHeader())

    def parse_issue(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        if is_first == 1:
            if len(repos_data) > 0:
                issue_id_last = repos_data[0]['id']
                issue_time_last = repos_data[0]['created_at']
                # store latest issue id
                try:
                    update_sql = "update moose_event_id set issue_id = %s , issue_time= %s where oss_id=%s"
                    self.cursor.execute(update_sql, (str(issue_id_last), str(issue_time_last), str(oss_id)))
                    self.dbObject.commit()
                except:
                    pass
        finish = 0
        for repos_per_data in repos_data:
            issue_id_current = repos_per_data['id']
            if int(self.oss_event_id[oss_id][1]) != 0 and int(self.oss_event_id[oss_id][1]) >= int(issue_id_current):
                finish = 1
                break
            create_time = repos_per_data['created_at']
            title = repos_per_data['title']
            body = repos_per_data['body']
            if body is None:
                body = ''
            if repos_per_data['state'] == 'closed':
                issue_state = 1
                close_time = repos_per_data['closed_at']
                if close_time is None:
                    close_time = ''
            else:
                issue_state = 0
                close_time = ''
            issue_user_type = repos_per_data['author_association']
            if issue_user_type == 'MEMBER' or issue_user_type == 'COLLABORATOR':
                core_issue = 1
            else:
                core_issue = 0
            issue_comment_count = repos_per_data['comments']
            if issue_comment_count is None:
                issue_comment_count = 0
            user_id = repos_per_data['user']['id']
            # statistic user
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.user_parse, headers=getHeader())
            body = [
                {
                    "measurement": "moose_issue",
                    "time": create_time,
                    "tags": {
                        "oss_id": oss_id,
                        "community_id": self.community_id[oss_id],
                        "issue_id": issue_id_current
                    },
                    "fields": {
                        "core_issue": core_issue,
                        "issue_state": issue_state,
                        "title": title,
                        "body": body,
                        "issue_comment_count": issue_comment_count,
                        "close_time": close_time,
                        "user_id": user_id
                    },
                }
            ]
            res = self.client.write_points(body)
        if finish != 1:
            listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
            if len(listLink_next_url) > 0:
                yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2, "oss_id": oss_id}, callback=self.parse_issue, headers=getHeader())

    def parse_issue_comment(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        if is_first == 1:
            if len(repos_data) > 0:
                issue_comment_id_last = repos_data[0]['id']
                issue_comment_time_last = repos_data[0]['created_at']
                # store latest issue comment id
                try:
                    update_sql = "update moose_event_id set issue_comment_id = %s , issue_comment_time= %s where oss_id=%s"
                    self.cursor.execute(update_sql, (str(issue_comment_id_last), str(issue_comment_time_last), str(oss_id)))
                    self.dbObject.commit()
                except:
                    pass
        finish = 0
        for repos_per_data in repos_data:
            issue_comment_id_current = repos_per_data['id']
            if int(self.oss_event_id[oss_id][5]) != 0 and int(self.oss_event_id[oss_id][5]) >= int(issue_comment_id_current):
                finish = 1
                break
            create_time = repos_per_data['created_at']
            body = repos_per_data['body']
            if body is None:
                body = ''

            issue_comment_user_type = repos_per_data['author_association']
            if issue_comment_user_type == 'MEMBER' or issue_comment_user_type == 'COLLABORATOR':
                core_issue_comment = 1
            else:
                core_issue_comment = 0

            user_id = repos_per_data['user']['id']
            # statistic user
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.user_parse, headers=getHeader())
            body = [
                {
                    "measurement": "moose_issue_comment",
                    "time": create_time,
                    "tags": {
                        "oss_id": oss_id,
                        "community_id": self.community_id[oss_id],
                        "issue_comment_id": issue_comment_id_current
                    },
                    "fields": {
                        "core_issue_comment": core_issue_comment,
                        "body": body,
                        "user_id": user_id
                    },
                }
            ]
            res = self.client.write_points(body)
        if finish != 1:
            listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
            if len(listLink_next_url) > 0:
                yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2, "oss_id": oss_id}, callback=self.parse_issue_comment, headers=getHeader())

    def parse_pullrequest(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        pull_url = response.meta['pull_url']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        if is_first == 1:
            if len(repos_data) > 0:
                pull_id_last = repos_data[0]['id']
                pull_time_last = repos_data[0]['created_at']
                # store latest pr id
                try:
                    update_sql = "update moose_event_id set pullrequest_id = %s , pullrequest_time= %s where oss_id=%s"
                    self.cursor.execute(update_sql, (str(pull_id_last), str(pull_time_last), str(oss_id)))
                    self.dbObject.commit()
                except:
                    pass
        finish = 0
        for repos_per_data in repos_data:
            pull_id_current = repos_per_data['id']
            pull_no = repos_per_data['number']
            if int(self.oss_event_id[oss_id][2]) != 0 and int(self.oss_event_id[oss_id][2]) >= int(pull_id_current):
                finish = 1
                break
            create_time = repos_per_data['created_at']
            title = repos_per_data['title']
            body = repos_per_data['body']
            if body is None:
                body = ''
            if repos_per_data['state'] == 'open':
                pull_state = 0
            elif repos_per_data['state'] == 'closed':
                pull_state = 1
            else:
                pull_state = 2

            close_time = repos_per_data['closed_at']
            if repos_per_data['merged_at'] is None:
                pull_merged = 0
                merged_time = ''
            else:
                pull_merged = 1
                merged_time = repos_per_data['merged_at']

            pull_user_type = repos_per_data['author_association']
            if pull_user_type == 'MEMBER' or pull_user_type == 'COLLABORATOR':
                core_pull = 1
            else:
                core_pull = 0
            # 进入详情页，计算comment数量和review comment数量
            pull_detail_url = pull_url + "/" + str(pull_no)
            pull_detail_html = requests.get(pull_detail_url, headers=getHeader()).text
            pull_datail_html_info = json.loads(pull_detail_html)
            if (pull_datail_html_info is not None and len(pull_datail_html_info) > 0 and "message" not in pull_datail_html_info):
                pull_comment_count = pull_datail_html_info['comments']
                if pull_comment_count is None:
                    pull_comment_count = 0
                pull_review_comment_count = pull_datail_html_info['review_comments']
                if pull_review_comment_count is None:
                    pull_review_comment_count = 0
            else:
                pull_comment_count = 0
                pull_review_comment_count = 0

            # 查询review
            pull_review_url = pull_url + "/" + str(pull_no) + "/reviews"
            pull_review_html = requests.get(pull_review_url, headers=getHeader()).text
            pull_review_html_info = json.loads(pull_review_html)
            core_review_count = 0
            if (pull_review_html_info is not None and len(pull_review_html_info) > 0 and "message" not in pull_review_html_info):
                pull_reviewed = 1
                for review in pull_review_html_info:
                    review_user_type = review['author_association']
                    if review_user_type == 'MEMBER' or review_user_type == 'COLLABORATOR':
                        core_review_count += 1
            else:
                pull_reviewed = 0
            # 查询review comment
            core_review_comment_count = 0
            if pull_review_comment_count > 0:
                pull_review_comment_url = pull_url + "/" + str(pull_no) + "/comments"
                pull_review_comment_html = requests.get(pull_review_comment_url, headers=getHeader()).text
                pull_review_comment_html_info = json.loads(pull_review_comment_html)
                if (pull_review_comment_html_info is not None and len(pull_review_comment_html_info) > 0 and "message" not in pull_review_comment_html_info):
                    for review_comment in pull_review_comment_html_info:
                        review_comment_user_type = review_comment['author_association']
                        if review_comment_user_type == 'MEMBER' or review_comment_user_type == 'COLLABORATOR':
                            core_review_comment_count += 1
                else:
                    core_review_comment_count = 0
            # statistic user
            user_exit = self.is_user_exit(repos_per_data['user']['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = repos_per_data['user']['url']
                yield scrapy.Request(owner_url, callback=self.user_parse, headers=getHeader())
            user_id = repos_per_data['user']['id']
            body = [
                {
                    "measurement": "moose_pull",
                    "time": create_time,
                    "tags": {
                        "oss_id": oss_id,
                        "community_id": self.community_id[oss_id],
                        "issue_id": pull_id_current
                    },
                    "fields": {
                        "core_pull": core_pull,
                        "pull_state": pull_state,
                        "pull_merged": pull_merged,
                        "pull_reviewed": pull_reviewed,
                        "title": title,
                        "body": body,
                        "pull_comment_count": pull_comment_count,
                        "pull_review_comment_count": pull_review_comment_count,
                        "close_time": close_time,
                        "merged_time": merged_time,
                        "user_id": user_id,
                        "core_review_count": core_review_count,
                        "core_review_comment_count": core_review_comment_count
                    },
                }
            ]
            res = self.client.write_points(body)
        if finish != 1:
            listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
            if len(listLink_next_url) > 0:
                yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2, "oss_id": oss_id, "pull_url": pull_url}, callback=self.parse_pullrequest, headers=getHeader())

        pass

    def parse_event(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        try:
            if is_first == 1:
                if len(repos_data) > 0:
                    event_id_last = repos_data[0]['id']
                    event_time_last = repos_data[0]['created_at']
                    # store latest event id
                    update_sql = r"update moose_event_id set event_id = " + str(
                        event_id_last) + ", event_time='" + event_time_last + "' where oss_id=" + str(oss_id)
                    self.cursor.execute(update_sql)
                    self.dbObject.commit()

            index_dict = dict()
            finish = 0
            for per_event in repos_data:
                event_id_current = per_event['id']
                oss_id = per_event['repo']['id']
                if int(self.oss_event_id[oss_id][0]) != 0 and int(self.oss_event_id[oss_id][0]) >= int(event_id_current):
                    finish = 1
                    break

                event_type = per_event['type']
                event_time = per_event['created_at'][:10]
                if event_type in index_dict:
                    if event_time in index_dict[event_type]:
                        index_dict[event_type][event_time] += 1
                    else:
                        index_dict[event_type].update({event_time: 1})
                else:
                    index_dict.update({event_type: {event_time: 1}})
            for index_type in index_dict:
                for index_time in index_dict[index_type]:
                    query = "select * from moose_index where index_type='" + index_type + "' and time='" + index_time + "' and oss_id='" + str(oss_id) + "' ;"
                    result = self.client.query(query).get_points()
                    index_count = index_dict[index_type][index_time]
                    try:
                        for point in result:
                            index_count += point[u'index_count']
                    except Exception as ex:
                        index_count = index_dict[index_type][index_time]
                    body = [
                        {
                            "measurement": "moose_index",
                            "time": index_time,
                            "tags": {
                                "oss_id": oss_id,
                                "community_id": self.community_id[oss_id],
                                "index_type": index_type
                            },
                            "fields": {
                                "index_count": index_count
                            },
                        }
                    ]
                    res = self.client.write_points(body)
            if finish != 1:
                listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
                if len(listLink_next_url) > 0:
                    yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2,"oss_id": oss_id}, callback=self.parse_event,
                                         headers=getHeader())
        except Exception as ex:
            print(ex)

    def parse_commit(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        if is_first == 1:
            if len(repos_data) > 0:
                commit_node_last = repos_data[0]['node_id']
                commit_time_last = repos_data[0]['commit']['author']['date']
                # store latest issue id
                try:
                    update_sql = "update moose_event_id set commit_id = %s , commit_time= %s where oss_id=%s"
                    self.cursor.execute(update_sql, (str(commit_node_last), str(commit_time_last), str(oss_id)))
                    self.dbObject.commit()
                except:
                    pass
        finish = 0
        for repos_per_data in repos_data:
            commit_node = repos_per_data['node_id']
            commit_time = repos_per_data['commit']['author']['date']
            if self.oss_event_id[oss_id][3] != 0 and self.oss_event_id[oss_id][3] >= commit_time:
                finish = 1
                break
            message = repos_per_data['commit']['message']
            if message is None:
                message = ''
            try:
                user_id = repos_per_data['author']['id']
            except:
                user_id = 0

            body = [
                {
                    "measurement": "moose_commit",
                    "time": commit_time,
                    "tags": {
                        "oss_id": oss_id,
                        "community_id": self.community_id[oss_id],
                        "commit_node": commit_node
                    },
                    "fields": {
                        "message": message,
                        "user_id": user_id
                    },
                }
            ]
            res = self.client.write_points(body)
        if finish != 1:
            listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
            if len(listLink_next_url) > 0:
                yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2, "oss_id": oss_id}, callback=self.parse_commit, headers=getHeader())

    def parse_commit_comment(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        try:
            is_first = response.meta['is_first']
        except Exception as ex:
            is_first = 1
        if is_first == 1:
            if len(repos_data) > 0:
                comment_id_last = repos_data[0]['id']
                comment_time_last = repos_data[0]['created_at']
                # store latest issue id
                try:
                    update_sql = "update moose_event_id set comment_id = %s , comment_time= %s where oss_id=%s"
                    self.cursor.execute(update_sql, (str(comment_id_last), str(comment_time_last), str(oss_id)))
                    self.dbObject.commit()
                except:
                    pass
        finish = 0
        for repos_per_data in repos_data:
            comment_id = repos_per_data['id']
            comment_time = repos_per_data['created_at']
            if int(self.oss_event_id[oss_id][4]) != 0 and int(self.oss_event_id[oss_id][4]) >= int(comment_id):
                finish = 1
                break
            body = repos_per_data['body']
            if body is None:
                body = ''
            commit_comment_user_type = repos_per_data['author_association']
            if commit_comment_user_type == 'MEMBER' or commit_comment_user_type == 'COLLABORATOR':
                core_commit_comment = 1
            else:
                core_commit_comment = 0
            try:
                user_id = repos_per_data['user']['id']
            except:
                user_id = 0
            body = [
                {
                    "measurement": "moose_comment",
                    "time": comment_time,
                    "tags": {
                        "oss_id": oss_id,
                        "community_id": self.community_id[oss_id],
                        "comment_id": comment_id
                    },
                    "fields": {
                        "body": body,
                        "user_id": user_id,
                        "core_commit_comment": core_commit_comment,
                    },
                }
            ]
            res = self.client.write_points(body)
        if finish != 1:
            listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
            if len(listLink_next_url) > 0: yield scrapy.Request(listLink_next_url[0], meta={"is_first": 2, "oss_id": oss_id}, callback=self.parse_commit_comment, headers=getHeader())

    def user_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        User_Info_item = MOOSEUser()
        User_Info_item['user_id'] = repos_data['id']
        User_Info_item['user_name'] = repos_data['login']
        if repos_data['name'] != None:
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
        cursor.execute("select * from moose_user where user_id=%s", (uid))
        result = cursor.fetchone()
        if result:
            return 1
        else:
            return 0