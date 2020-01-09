import datetime
from sqlobject import *
from conf import config_operate
uri = config_operate.get_dbconfig_uri()
sqlhub.processConnection = connectionForURI(uri)


# oss community api
class MOOSECommunityApi(SQLObject):
    community_name = StringCol(length = 50, notNone = True)
    get_oss_list_api = StringCol(length = 255, notNone = True)
    get_oss_single_api = StringCol(length = 255, notNone = True)
    git_api = StringCol(length=255)


class MOOSEMetadata(SQLObject):
    oss_id = IntCol(length=50)
    oss_from = IntCol(length=11)
    oss_name = StringCol(length = 50)
    oss_fullname = StringCol(length = 100, unique = True)
    oss_create_time = StringCol(length = 50)
    oss_git_url = StringCol(length = 200)
    oss_git_tool = StringCol(length = 30)
    oss_repo_url = StringCol(length = 200)
    oss_homepage = StringCol(length = 100)
    oss_license = StringCol(length = 100)
    oss_description = StringCol(length = 5000)
    oss_local_path = StringCol(length = 50)
    oss_line_count = IntCol(length = 50)
    oss_developer_count = IntCol(length = 50)
    oss_file_count = IntCol(length = 50)
    oss_commit_count = IntCol(length = 50)
    oss_lastupdate_time = StringCol(length = 50)
    oss_owner_id = IntCol(length = 50)
    oss_owner_type = StringCol(length = 100)
    oss_star = IntCol(length=11)
    oss_fork = IntCol(length=11)
    oss_main_language = StringCol(length = 50)
    oss_language_count = IntCol(length=11)
    oss_owner_id = IntCol(length = 11)
    oss_owner_type = StringCol(length = 11)
    oss_size = IntCol(length = 11)
    oss_lastupdate_time = StringCol(length = 50)
    has_wiki = IntCol(length = 11)
    readme = StringCol(length = 5000)
    oss_all_day = IntCol(length = 11)
    oss_active_day = IntCol(length = 11)

class MOOSElibTopic(SQLObject):
    oss_id = IntCol(length = 11)
    topic = StringCol(length = 100)


class MOOSEGeneral(SQLObject):
    project_name = StringCol(length = 255)
    generated = StringCol(length = 255)
    generator = StringCol(length = 255)
    report_period = StringCol(length = 255)
    age_days = StringCol(length = 255)
    total_files = StringCol(length = 255)
    total_lines_of_code = StringCol(length = 255)
    total_commits = StringCol(length = 255)
    authors = StringCol(length = 255)
    oss_id = IntCol(length = 11)

class MOOSEActivityWeek (SQLObject):
    week=IntCol(length=11)
    commits=IntCol(length=11)
    oss_id = IntCol(length=11)


class MOOSEActivityHour (SQLObject):
    hour = IntCol(length = 11)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityDay(SQLObject):
    day = StringCol(length = 255)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityHourOfWeek(SQLObject):
    weekday_hour = StringCol(length = 255)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityMonth(SQLObject):
    month = StringCol(length =255)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityYear(SQLObject):
    year = IntCol(length = 11)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityYearMonth(SQLObject):
    yearmonth = StringCol(length = 255)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEActivityTimezone(SQLObject):
    timezone = StringCol(length = 255)
    commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEAuthorList(SQLObject):
    user_id= IntCol (length = 11)
    author = StringCol(length = 255)
    commits = IntCol(length = 11)
    commits_frac = StringCol(length = 255)
    lines_added = IntCol(length = 11)
    lines_removed = IntCol(length = 11)
    first_commit = StringCol(length = 255)
    last_commit = StringCol(length = 255)
    age = StringCol(length = 255)
    active_days = IntCol(length = 11)
    by_commits = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEAuthorCumulated(SQLObject):
    date = StringCol(length = 255)
    author = StringCol(length = 255)
    cumulated_commits = IntCol(length = 11)
    cumulated_lines = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEAuthorMonth(SQLObject):
    month = StringCol(length = 255)
    author = StringCol(length = 255)  
    commits = StringCol(length = 255)
    next_top5 = StringCol(length = 255)
    author_number = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEAuthorYear(SQLObject):
    year = IntCol(length = 11)
    author = StringCol(length = 255)
    commits = StringCol(length = 255)
    next_top5 = StringCol(length = 255)
    author_number = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEDomain(SQLObject):
    domain = StringCol(length=255)
    commits = IntCol(length=11)
    commits_frac = StringCol(length=255)
    oss_id = IntCol(length=11)


class MOOSEFileDateCount(SQLObject):
    date = StringCol(length = 255)
    files = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSEFileExtension(SQLObject):
    extension = StringCol(length = 255)
    files = StringCol(length = 255)
    line = StringCol(length = 255)
    filesdividelines = IntCol(length = 11)
    oss_id = IntCol(length = 11)
 
class MOOSELineDateCount(SQLObject):
    date = StringCol(length = 255)
    line = IntCol(length = 11)
    oss_id = IntCol(length = 11)


class MOOSETag(SQLObject):
    name = StringCol(length = 255)
    date = StringCol(length = 255)
    commits = IntCol(length = 11)
    authors = StringCol(length = 3000)
    oss_id = IntCol(length = 11)


class MOOSEDeveloper(SQLObject):
    oss_id = IntCol(length = 11)
    user_id = IntCol(length = 20)
    update_time = StringCol(length = 255)
    user_commit_count = IntCol(length = 11)


class MOOSECommunity(SQLObject):
    user_id = IntCol(length=11)
    community_name = StringCol(length=255)
    create_time = DateTimeCol()
    status = IntCol(length=11)


class MOOSECommunityList(SQLObject):
    community_id = IntCol(length=11)
    oss_id = IntCol(length=11)
    meta_id = IntCol(length=11)
    add_time = DateTimeCol()
    status = IntCol(length=11)
    oss_name = StringCol(length=255)


class MOOSEStatistic(SQLObject):
    community_id = IntCol(length=11)
    issue_count = IntCol(length=11)
    issue_close_count = IntCol(length=11)
    pull_count = IntCol(length=11)
    pull_merged_count = IntCol(length=11)
    loc = IntCol(length=11)
    doc = IntCol(length=11)
    foc = IntCol(length=11)
    coc = IntCol(length=11)
    issue_comment_count = IntCol(length=11)
    issue_close_time = FloatCol()
    core_issue_count = IntCol(length=11)
    update_time = StringCol(length=255)
    language_count = IntCol(length=11)
    all_days = IntCol(length=11)
    active_days = IntCol(length=11)
    pull_comment_count = IntCol(length=11)
    pull_review_count = IntCol(length=11)
    pull_review_comment_count = IntCol(length=11)
    core_pull_count = IntCol(length=11)
    core_review_count = IntCol(length=11)
    core_review_comment_count = IntCol(length=11)
    pull_merged_time = FloatCol()
    core_developer_count = IntCol(length=11)
    fork_count = IntCol(length=11)
    star_count = IntCol(length=11)
    core_developer_change = FloatCol()
    pull_change = FloatCol()
    issue_change = FloatCol()
    commit_count = IntCol(length=11)
    commit_comment_count = IntCol(length=11)
    core_commit_comment_count = IntCol(length=11)
    core_issue_comment_count = IntCol(length=11)

class MOOSEIssue(SQLObject):
    issue_user_type = StringCol(length=100)
    issue_state = IntCol(length=11)
    oss_id = IntCol(length=11)
    user_id = IntCol(length=11)
    issue_close_time = StringCol(length=100)
    issue_create_time = StringCol(length=100)
    update_time = StringCol(length=100)
    issue_comment_count = IntCol(length=11)
    issue_id = IntCol(length=11)
    issue_number = IntCol(length=11)
    issue_update_time = StringCol(length=100)
    issue_body = StringCol(length=5000)
    issue_title = StringCol(length=5000)


class MOOSEPulls(SQLObject):
    pull_id = IntCol(length=11)
    pull_number = IntCol(length=11)
    pull_state = IntCol(length=11)
    pull_author_association = StringCol(length=100)
    pull_create_time = StringCol(length=100)
    pull_update_time = StringCol(length=100)
    pull_closed_time = StringCol(length=100)
    pull_merged_time = StringCol(length=100)
    pull_is_merged = IntCol(length=11)
    update_time = StringCol(length=100)
    user_id = IntCol(length=11)
    oss_id = IntCol(length=11)
    pull_title = StringCol(length=100)
    pull_body = StringCol(length=100)
    pull_is_reviewed = IntCol(length=11)
    pull_comments = IntCol(length=11)
    review_comments = IntCol(length=11)
    request_reviewer = StringCol(length=500)


class MOOSEIssueComment(SQLObject):
    issue_comment_id = IntCol(length=11)
    user_id = IntCol(length=11)
    created_time = StringCol(length=100)
    body = StringCol(length=5000)
    author_association = StringCol(length=100)
    oss_id = IntCol(length=11)
    update_time = StringCol(length=100)



class MOOSEStatisticCommitYearmonth(SQLObject):
    community_id = IntCol(length=11)
    yearmonth = StringCol(length=50)
    commits_count = IntCol(length=11)


class MOOSEStatisticIssueYearmonth(SQLObject):
    community_id = IntCol(length=11)
    yearmonth = StringCol(length=50)
    issue_count = IntCol(length=11)
    close_issue_count = IntCol(length=11)

class MOOSEStatisticPullYearmonth(SQLObject):
    community_id = IntCol(length=11)
    yearmonth = StringCol(length=50)
    pull_count = IntCol(length=11)
    merged_pull_count = IntCol(length=11)


class MOOSEStatisticCommitHourday(SQLObject):
    community_id = IntCol(length=11)
    day = IntCol(length=11)
    commit_count = IntCol(length=11)
    hour = IntCol(length=11)


class MOOSEStatisticAuthor(SQLObject):
    community_id = IntCol(length=11)
    oss_id = IntCol(length=11)
    commit_count = IntCol(length=11)
    last_commit_time = StringCol(length=100)
    user_id = IntCol(length=11)
    user_name = StringCol(length=100)


class MOOSEUser(SQLObject):
    avatar_url = StringCol(length=500)
    user_name = StringCol(length=100)
    user_fullname = StringCol(length=100)
    user_id = IntCol(length=11)


class MOOSEStatisticAuthorYearmonth(SQLObject):
    yearmonth = StringCol(length=50)
    community_id = IntCol(length=11)
    developer_count = IntCol(length=11)


class MOOSEStatisticSentiment(SQLObject):
    community_id = IntCol(length=11)
    yearmonth = StringCol(length=50)
    neg = IntCol(length=11)
    pos = IntCol(length=11)
    neu = IntCol(length=11)
    ave = IntCol(length=11)