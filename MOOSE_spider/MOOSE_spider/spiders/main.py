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
    cursor.execute("select oss_name, oss_id, community_id from moose_community_list")
    results = cursor.fetchall()
    for result in results:
        scrapyed_list.append("https://api.github.com/repos/" + result[0])
    repo_index = 0
    start_urls = [scrapyed_list[0]]

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
                if oss_homepage is None:
                    oss_homepage = ''
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
                    pre = re.compile('>(.*?)<')
                    readme = ''.join(pre.findall(readme))
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

            # developer data crawl
            contributors_url = repos_data['contributors_url'] + "?per_page=100"
            yield scrapy.Request(contributors_url, meta={"oss_id": oss_id}, callback=self.contributors_parse, headers=getHeader())


            # topic data crawl
            topics_response = requests.get(url=repos_data['url'] + "/topics", headers=getHeader())
            topics_text = topics_response.text
            topic_jsonobj = json.loads(topics_text)
            topic_items = MOOSEStatisticsTopic()
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
        if self.repo_index <= len(self.scrapyed_list) - 1:
            yield scrapy.Request(self.scrapyed_list[self.repo_index], callback=self.parse, headers=getHeader())

    def contributors_parse(self, response):
        repos_data = json.loads(response.body.decode('utf-8'))
        repos_header = response.headers
        oss_id = response.meta['oss_id']
        contributors_items = MOOSEDeveloper()
        for contributors in repos_data:
            contributors_items['oss_id'] = oss_id
            contributors_items['user_id'] = contributors['id']
            contributors_items['user_commit_count'] = contributors['contributions']
            contributors_items['update_time'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            yield contributors_items
            # statistic user
            user_exit = self.is_user_exit(contributors['id'])
            if (user_exit == 1):
                pass
            else:
                owner_url = contributors['url']
                yield scrapy.Request(owner_url, callback=self.user_parse, headers=getHeader())

        listLink_next_url = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)', str(repos_header))
        if len(listLink_next_url) > 0:
            yield scrapy.Request(listLink_next_url[0], meta={"oss_id": oss_id},callback=self.contributors_parse, headers=getHeader())

    def user_parse(self, response):
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
        cursor.execute("select * from moose_user where user_id=%s", (uid))
        result = cursor.fetchone()
        if result:
            return 1
        else:
            return 0


