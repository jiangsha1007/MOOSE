# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import datetime
from MOOSE_spider import settings
from MOOSE_spider.items import *
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
class OsslibSpiderPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        if isinstance(item, MOOSEIssue):
            cursor.execute("select * from MOOSE_issue where issue_id=%s and issue_number = %s",
                           (item['issue_id'], item['issue_number']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_issue set  oss_id =%s,issue_state = %s,user_id=%s, " \
                      "issue_user_type = %s,issue_create_time = %s,issue_update_time = %s," \
                      "issue_close_time = %s,issue_comment_count = %s,update_time=%s ,issue_body=%s,issue_title=%s  " \
                      " where issue_id = %s and issue_number=%s"
                try:
                    cursor.execute(sql, (item['oss_id'], item['issue_state'], item['user_id'], item['issue_user_type'],
                                         item['issue_create_time'], item['issue_update_time'], item['issue_close_time'],
                                         item['issue_comment_count'], item['update_time'], item['issue_body'],
                                         item['issue_title'],
                                         item['issue_id'], item['issue_number']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_issue(oss_id , issue_state , user_id,issue_user_type," \
                      "issue_create_time,issue_update_time,issue_close_time,issue_comment_count,update_time," \
                      "issue_id,issue_number,issue_body,issue_title) " \
                      "VALUES(%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item['oss_id'], item['issue_state'], item['user_id'], item['issue_user_type'],
                                         item['issue_create_time'], item['issue_update_time'], item['issue_close_time'],
                                         item['issue_comment_count'], item['update_time'],
                                         item['issue_id'], item['issue_number'], item['issue_body'],
                                         item['issue_title']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(item)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEPulls):

            cursor.execute("select * from MOOSE_pulls where pull_id=%s and pull_number = %s",
                           (item['pull_id'], item['pull_number']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_pulls set  oss_id =%s,pull_state = %s,user_id=%s, " \
                      "pull_author_association = %s,pull_create_time = %s,pull_update_time = %s," \
                      "pull_closed_time = %s,pull_merged_time = %s,pull_is_merged = %s,pull_title = %s," \
                      "pull_body = %s,pull_is_reviewed = %s,pull_comments = %s,review_comments = %s,request_reviewer=%s,update_time=%s " \
                      " where pull_id = %s and pull_number=%s"
                try:

                    cursor.execute(sql, (
                    item['oss_id'], item['pull_state'], item['user_id'], item['pull_author_association'],
                    item['pull_created_at'], item['pull_update_at'], item['pull_closed_at'],
                    item['pull_merged_at'], item['pull_is_merged'], item['pull_title'],item['pull_body'],
                    item['pull_is_reviewed'],item['pull_comments'],item['review_comments'],item['request_reviewer'],item['update_time'],
                    item['pull_id'], item['pull_number']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_pulls(oss_id , pull_state , user_id,pull_author_association," \
                      "pull_create_time,pull_update_time,pull_closed_time,pull_merged_time,pull_is_merged,pull_title," \
                      "pull_body,pull_is_reviewed,update_time,pull_comments,review_comments,request_reviewer," \
                      "pull_id,pull_number) " \
                      "VALUES(%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (
                    item['oss_id'], item['pull_state'], item['user_id'], item['pull_author_association'],
                    item['pull_created_at'], item['pull_update_at'], item['pull_closed_at'],
                    item['pull_merged_at'], item['pull_is_merged'], item['pull_title'],item['pull_body'],
                    item['pull_is_reviewed'],item['update_time'],item['pull_comments'],item['review_comments'],item['request_reviewer'],
                    item['pull_id'], item['pull_number']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEPullsReviewers):
            cursor.execute("select * from MOOSE_pulls_review where review_id=%s ",
                           (item['review_id']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_pulls_review set  is_requested =%s,reviewed_time =%s,update_time =%s,author_association=%s " \
                      "where review_id=%s "
                try:
                    cursor.execute(sql, (item['is_requested'],item['reviewed_time'],item['update_time'],item['author_association'],
                                         item['review_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_pulls_review(review_id,oss_id , reviewer_id,pull_id,is_requested,reviewed_time,update_time,author_association) " \
                      "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item['review_id'], item['oss_id'], item['reviewer_id'], item['pull_id'],
                                         item['is_requested'], item['reviewed_time'], item['update_time'], item['author_association']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsComment):
            cursor.execute("select * from MOOSE_statistic where oss_id=%s", (item['oss_id']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_statistic set  commit_comment_count =%s,core_commit_comment_count =%s " \
                      "where oss_id=%s "
                try:
                    cursor.execute(sql, (item['commit_comment_count'], item['core_commit_comment_count'],
                                         item['oss_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic(oss_id, commit_comment_count, core_commit_comment_count ) " \
                      "VALUES(%s,%s)"
                try:
                    cursor.execute(sql, (item['oss_id'], item['commit_comment_count'], item['core_commit_comment_count']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, OsslibDeveloper):
            cursor.execute("select * from osslib_developer where oss_id=%s and user_id = %s",
                           (item['oss_id'], item['user_id']))
            result = cursor.fetchone()
            if result:
                sql = "update osslib_developer set  user_commit_count =%s,update_time = %s" \
                      "where oss_id = %s and user_id=%s"
                try:
                    cursor.execute(sql, (item['user_commit_count'], item['update_time'], item['oss_id'], item['user_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into osslib_developer(oss_id, user_id, user_commit_count, update_time) " \
                      "VALUES(%s,%s,%s, %s)"
                try:
                    cursor.execute(sql, (item['oss_id'], item['user_id'], item['user_commit_count'], item['update_time']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MooseMetadata):
            cursor.execute("select * from MOOSE_metadata where oss_id=%s",
                           (item['oss_id']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_metadata set oss_language=%s,oss_name=%s, oss_fullname =%s,oss_language_count =%s," \
                      "oss_star=%s, oss_fork=%s, oss_subscriber=%s, oss_owner_id=%s, oss_owner_type=%s, oss_size=%s, oss_main_language=%s," \
                      "oss_create_time=%s, oss_description=%s, oss_license=%s, oss_git_url=%s, oss_git_tool=%s, oss_repo_url=%s," \
                      "oss_homepage=%s, has_wiki=%s, has_pages=%s, readme=%s, oss_lastupdate_time=%s, update_time=%s  where oss_id = %s "
                try:
                    cursor.execute(sql, (item['oss_language'], item['oss_name'], item['oss_fullname'], item['oss_language_count'], item['oss_star'],
                                         item['oss_fork'], item['oss_subscriber'], item['oss_owner_id'],  item['oss_owner_type'],
                                         item['oss_size'], item['oss_main_language'], item['oss_create_time'],  item['oss_description'],
                                         item['oss_license'], item['oss_git_url'], item['oss_git_tool'],  item['oss_repo_url'],
                                         item['oss_homepage'], item['has_wiki'], item['has_pages'],  item['readme'],
                                         item['oss_lastupdate_time'], item['update_time'], item['oss_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_metadata(oss_id, oss_language, oss_language_count, oss_name, oss_fullname, oss_star, oss_fork," \
                      "oss_subscriber, oss_owner_id, oss_owner_type, oss_size, oss_main_language, oss_create_time, oss_description," \
                      "oss_license, oss_git_url, oss_git_tool, oss_repo_url, oss_homepage, has_wiki, has_pages, readme," \
                      "oss_lastupdate_time, update_time) VALUES(%s,%s,%s, %s, %s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql, (item['oss_id'], item['oss_language'], item['oss_language_count'], item['oss_name'], item['oss_fullname'], item['oss_star'],
                                         item['oss_fork'], item['oss_subscriber'], item['oss_owner_id'], item['oss_owner_type'], item['oss_size'],
                                         item['oss_main_language'], item['oss_create_time'], item['oss_description'], item['oss_license'], item['oss_git_url'],
                                         item['oss_git_tool'], item['oss_repo_url'], item['oss_homepage'], item['has_wiki'], item['has_pages'],
                                         item['readme'], item['oss_lastupdate_time'], item['update_time']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEIssueComment):
            cursor.execute("select * from MOOSE_issue_comment where issue_comment_id=%s and oss_id=%s ",
                           (item['issue_comment_id'],item['oss_id']))
            result = cursor.fetchone()
            if result:
                pass
            else:
                sql = "insert into MOOSE_issue_comment(oss_id, issue_comment_id, user_id, created_time, body, author_association," \
                      "update_time) VALUES(%s,%s,%s, %s, %s,%s,%s)"
                try:
                    cursor.execute(sql, (item['oss_id'], item['issue_comment_id'], item['user_id'], item['created_time'], item['body'], item['author_association'],
                                         item['update_time']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEUser):
            cursor.execute("select * from MOOSE_user where user_id=%s", (item['user_id']))
            result = cursor.fetchone()
            if result:

                sql = "update MOOSE_user set user_name=%s , user_fullname =%s , " \
                      "avatar_url=%s,follows_count=%s,repos_count=%s ,blog_url=%s ,email_url=%s ," \
                      "org_member_count=%s,user_type =%s,user_create_time=%s ,user_update_time=%s ,update_time =%s ," \
                      "user_location = %s,user_company = %s where user_id =%s"
                try:
                    cursor.execute(sql, (item['user_name'], item['user_fullname'],
                                         item['avatar_url'], item['follows_count'], item['repos_count'],
                                         item['blog_url'], item['email_url'],
                                         item['org_member_count'], item['user_type'], item['user_create_time'],
                                         item['user_update_time'], item['update_time'], item['location'],
                                         item['company'],
                                         item['user_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()

                #pass
            else:
                sql = "insert into MOOSE_user(user_id , user_name , user_fullname , " \
                      "avatar_url,follows_count,repos_count ,blog_url ,email_url ," \
                      "org_member_count,user_type ,user_create_time ,user_update_time ,update_time," \
                      "user_location,user_company)" \
                      " VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['user_id'], item['user_name'], item['user_fullname'],
                                         item['avatar_url'], item['follows_count'], item['repos_count'],
                                         item['blog_url'], item['email_url'],
                                         item['org_member_count'], item['user_type'], item['user_create_time'],
                                         item['user_update_time'], item['update_time'], item['location'],
                                         item['company']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsIssue):
            cursor.execute("select * from MOOSE_statistic where oss_id=%s", (item['oss_id']))
            result = cursor.fetchone()
            if result:

                sql = "update MOOSE_statistic set issue_count=%s , issue_comment_count =%s , " \
                      "issue_close_count=%s,issue_close_time=%s,core_issue_count=%s where oss_id =%s"
                try:
                    cursor.execute(sql, (item['issue_count'], item['issue_comment_count'],
                                         item['issue_close_count'], item['issue_close_time'], item['core_issue_count'],
                                         item['oss_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic(oss_id , issue_count , issue_comment_count , " \
                      "issue_close_count,issue_close_time,core_issue_count) " \
                      " VALUES (%s,%s,%s,%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['issue_count'], item['issue_comment_count'],
                                         item['issue_close_count'], item['issue_close_time'], item['core_issue_count']
                                        ))
                    cursor.connection.commit()
                except BaseException as e:
                    print(286)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsPull):
            cursor.execute("select * from MOOSE_statistic where oss_id=%s", (item['oss_id']))
            result = cursor.fetchone()
            if result:
                sql = "update MOOSE_statistic set pull_count=%s , pull_merged_count =%s, pull_comment_count=%s, pull_review_comment_count=%s," \
                      "pull_review_count=%s, core_pull_count=%s, pull_merged_time=%s, core_review_comment_count=%s, core_review_count=%s where oss_id =%s"
                try:
                    cursor.execute(sql, (item['pull_count'], item['pull_merged_count'], item['pull_comment_count'], item['pull_review_comment_count'],
                                         item['pull_review_count'], item['core_pull_count'], item['pull_merged_time'], item['core_review_comment_count'],
                                         item['core_review_count'], item['oss_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic(oss_id, pull_count, pull_merged_count, pull_comment_count, pull_review_comment_count, " \
                      "pull_review_count, core_pull_count, pull_merged_time, core_review_comment_count, core_review_count) " \
                      " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['pull_count'], item['pull_merged_count'], item['pull_comment_count'], item['pull_review_comment_count'],
                                         item['pull_review_count'], item['core_pull_count'], item['pull_merged_time'], item['core_review_comment_count'],
                                        item['core_review_count']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(313)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsCommit):
            cursor.execute("select * from MOOSE_statistic where oss_id=%s", (item['oss_id']))
            result = cursor.fetchone()
            if result:

                sql = "update MOOSE_statistic set commit_count=%s where oss_id =%s"
                try:
                    cursor.execute(sql, (item['commit_count'], item['oss_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic(oss_id , commit_count ) " \
                      " VALUES (%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['commit_count']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(286)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsIssueMonth):
            cursor.execute("select issue_count,close_issue_count from MOOSE_statistic_issue_yearmonth where oss_id=%s and yearmonth=%s", (item['oss_id'], item['yearmonth']))
            result = cursor.fetchone()
            if result:
                issue_count = result[0]
                close_issue_count = result[1]
                issue_count += item['issue_count']
                close_issue_count += item['close_issue_count']
                sql = "update MOOSE_statistic_issue_yearmonth set issue_count=%s , close_issue_count =%s " \
                      " where oss_id =%s and yearmonth =%s"
                try:
                    cursor.execute(sql, (issue_count, close_issue_count, item['oss_id'], item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic_issue_yearmonth(oss_id, issue_count, close_issue_count, " \
                      "yearmonth) " \
                      " VALUES (%s,%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['issue_count'], item['close_issue_count'],
                                         item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(341)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsCommitMonth):
            cursor.execute("select commit_count from MOOSE_statistic_commit_yearmonth where oss_id=%s and yearmonth=%s", (item['oss_id'], item['yearmonth']))
            result = cursor.fetchone()
            if result:
                commit_count = result[0]
                commit_count += item['commit_count']
                sql = "update MOOSE_statistic_commit_yearmonth set commit_count=%s " \
                      " where oss_id =%s and yearmonth =%s"
                try:
                    cursor.execute(sql, (commit_count, item['oss_id'], item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic_commit_yearmonth(oss_id, commit_count, " \
                      "yearmonth) " \
                      " VALUES (%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['commit_count'],
                                         item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(341)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsPullMonth):
            cursor.execute("select pull_count,merged_pull_count from MOOSE_statistic_pull_yearmonth where oss_id=%s and yearmonth=%s", (item['oss_id'], item['yearmonth']))
            result = cursor.fetchone()
            if result:
                pull_count = result[0]
                merged_pull_count = result[1]
                pull_count += item['pull_count']
                merged_pull_count += item['merged_pull_count']
                sql = "update MOOSE_statistic_pull_yearmonth set pull_count=%s , merged_pull_count =%s " \
                      " where oss_id =%s and yearmonth =%s"
                try:
                    cursor.execute(sql, (pull_count, merged_pull_count, item['oss_id'], item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(357)
                    print(e)
                    dbObject.rollback()
            else:
                sql = "insert into MOOSE_statistic_pull_yearmonth(oss_id, pull_count, merged_pull_count, " \
                      "yearmonth) " \
                      " VALUES (%s,%s,%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['pull_count'], item['merged_pull_count'],
                                         item['yearmonth']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(369)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsUserRepo):
            cursor.execute("select * from MOOSE_user_repo where oss_id=%s and user_id=%s", (item['oss_id'], item['user_id']))
            result = cursor.fetchone()
            if result:
                pass
            else:
                sql = "insert into MOOSE_user_repo(oss_id, user_id ) " \
                      " VALUES (%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['user_id']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(384)
                    print(e)
                    dbObject.rollback()
        elif isinstance(item, MOOSEStatisticsTopic):
            cursor.execute("select * from MOOSE_topic where oss_id=%s and topic=%s", (item['oss_id'], item['topic']))
            result = cursor.fetchone()
            if result:
                pass
            else:
                sql = "insert into MOOSE_topic(oss_id, topic ) " \
                      " VALUES (%s,%s)"
                try:

                    cursor.execute(sql, (item['oss_id'], item['topic']))
                    cursor.connection.commit()
                except BaseException as e:
                    print(399)
                    print(e)
                    dbObject.rollback()
        return item
