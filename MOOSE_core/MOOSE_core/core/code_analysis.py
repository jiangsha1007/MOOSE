# -*- coding: utf8 -*-
from model.common_model import *
from core.common_git import *
from core.datacollector import *
from core.common import *
from core.statistics import *
from apscheduler.schedulers.background import BlockingScheduler
import datetime
import time
import os
from core.git import *

# 代码分析
class CodeAnalysis:
    def __init__(self):
        manager = get_thread_task_queue('getcoude_queue')
        self.task_queue = manager.getcoude_queue()

    #get code and analysis
    def code_analysis(self):
        print("new")
        oss_info = MOOSEMetadata.select(MOOSEMetadata.q.oss_git_url != "")
        for per_oss_info in oss_info:
            if per_oss_info.oss_git_url != '':
                trans_info = []
                trans_info.append(per_oss_info.oss_name)
                trans_info.append(per_oss_info.oss_git_url)
                trans_info.append(per_oss_info.oss_git_tool)
                trans_info.append(per_oss_info.id)
                self.task_queue.put(trans_info)
        for i in range(1):
            p = multiprocessing.Process(target=self._code_analysis_process, args=(self.task_queue, i,))
            p.start()
        p.join()

    def _code_analysis_process(self, q, i):
        time1 = time.clock()
        while True:
            if q.empty():
                print('waiting')
                time.sleep(3)
                time2 = time.clock()
                if time2-time1 >= 5:
                    break
                continue
            info = q.get()
            oss_name = info[0]
            oss_git_url = info[1]
            oss_git_tool = info[2]
            oss_id = info[3]
            return_info = -1
            print(oss_id)

            try:
                if oss_git_tool == 'Git':
                    local_path = os.path.join('data', oss_name)
                    repo = GitRepository(local_path, oss_git_url)
                    branch_list = repo.branches()
                    #repo.change_to_branch(branch_list[len(branch_list)-1])
                    repo.pull()
                    return_info = 1
                    #return_info = get_repo_by_git('data/'+oss_name, oss_git_url)#'git://git.code.sf.net'
                elif oss_git_tool == 'SVN':
                    return_info = get_repo_by_svn('data/' + oss_name, 'https://svn.code.sf.net' + oss_git_url)
            except:
                pass
            finally:
                if return_info == 1:
                    oss_info = MOOSEMetadata.get(oss_id)
                    oss_info.oss_local_path = 'data/' + oss_name

                time1 = time.clock()
                self._analysis(oss_id)
          

    def _analysis(self, oss_id):
        format = '%Y-%m-%d %H:%M:%S'
        Year = int(datetime.datetime.now().strftime(format)[:4])
        weekdays = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        print('analysis')
        for oss_info in MOOSEMetadata.select(MOOSEMetadata.q.id == oss_id):
            prevdir = os.getcwd()
            users = MOOSEDeveloper.select(MOOSEDeveloper.q.oss_id == oss_info.oss_id)
            sorted(users, key=lambda user: user.user_commit_count)
            user_id = []
            for info in users:
                user_id.append(info.user_id)
            count = 0;
      
            print('********************************************')
            if oss_info.oss_local_path != '':
                try:
                    gitpath = oss_info.oss_local_path
                    absgitpath = os.path.abspath(gitpath)
                    data = GitDataCollector()
                    data.collect(absgitpath)
                    data.refine()
                   
                    oss_info.oss_line_count = data.getTotalLOC()
                    oss_info.oss_developer_count = data.getTotalAuthors()
                    oss_info.oss_file_count = data.getTotalFiles()
                    oss_info.oss_commit_count = data.getTotalCommits()
                    oss_info.oss_all_day = data.getCommitDeltaDays()
                    oss_info.oss_active_day = len(data.getActiveDays())
                    
                    #General表
                    for info in MOOSEGeneral.select(MOOSEGeneral.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)                                        
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    item['project_name'] = data.projectname
                    item['generated'] = '%s (in %d seconds)'%(datetime.datetime.now().strftime(format), time.time() - data.getStampCreated())
                    item['generator'] = 'GitStats  (version %s), %s ' % (getversion(), getgitversion() )
                    item['report_period'] = ' %s to %s ' % (data.getFirstCommitDate().strftime(format), data.getLastCommitDate().strftime(format))
                    item['age_days'] = '%d days, %d active days (%3.2f%%) ' % (data.getCommitDeltaDays(), len(data.getActiveDays()), (100.0 * len(data.getActiveDays()) / data.getCommitDeltaDays()))
                    item['total_files'] = '%d' % (data.getTotalFiles())
                    item['total_lines_of_code'] = 'Lines of Code %s (%d added, %d removed)' % (data.getTotalLOC(), data.total_lines_added, data.total_lines_removed)
                    item['total_commits'] = ' %s (average %.1f commits per active day, %.1f per all days) ' % (data.getTotalCommits(), float(data.getTotalCommits()) / len(data.getActiveDays()), float(data.getTotalCommits()) / data.getCommitDeltaDays())
                    item['authors'] = '%s (average %.1f commits per author) ' % (data.getTotalAuthors(), (1.0 * data.getTotalCommits()) / data.getTotalAuthors())
                    MOOSEGeneral(**item)
                     
                    #Activity
                    #32week表
                    for info in MOOSEActivityWeek.select(MOOSEActivityWeek.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    WEEKS = 32
                    now = datetime.datetime.now()
                    deltaweek = datetime.timedelta(7)
                    stampcur = now
                    weeks=[]
                    for i in range(0, WEEKS):
                        weeks.append(stampcur.strftime('%Y-%W'))
                        stampcur -= deltaweek
                    for i in range(0, WEEKS):
                        if weeks[i] in data.activity_by_year_week:
                            commits = data.activity_by_year_week[weeks[i]]
                            item['week'] = i+1
                            item['commits'] = commits
                            MOOSEActivityWeek(**item)
                 
                
                    #24hour表
                    for info in MOOSEActivityHour.select(MOOSEActivityHour.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    hour_of_day = data.getActivityByHourOfDay()
                    for i in range(0,24):
                        if i in hour_of_day:
                            item['commits'] = hour_of_day[i]
                            item['hour'] = i
                            MOOSEActivityHour(**item)
                     
                    #7day表
                    for info in MOOSEActivityDay.select(MOOSEActivityDay.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    day_of_week = data.getActivityByDayOfWeek()
                    for i in range(0,7):
                        if i in day_of_week:
                            item['commits'] = day_of_week[i]
                            item['day'] = weekdays[i]
                            MOOSEActivityDay(**item)
                        
               
                    #hour_week表
                    for info in MOOSEActivityHourOfWeek.select(MOOSEActivityHourOfWeek.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for weekday in range(0, 7):
                        for hour in range(0, 24):
                            try:
                                commits = data.activity_by_hour_of_week[weekday][hour]
                                item['commits'] = commits
                                item['weekday_hour'] = '%s_%d'%(weekdays[weekday],hour)                                 
                                MOOSEActivityHourOfWeek(**item)
                            except KeyError:
                                pass
                  
                    
                    #month表
                    for info in MOOSEActivityMonth.select(MOOSEActivityMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for mm in range(1, 13):
                        if mm in data.activity_by_month_of_year:
                            commits = data.activity_by_month_of_year[mm]
                            item['commits'] = commits
                            item['month'] = months[mm-1]
                            MOOSEActivityMonth(**item) 
               
                    #year表
                    for info in MOOSEActivityYear.select(MOOSEActivityYear.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yy in reversed(sorted(data.commits_by_year.keys())): 
                        commits = data.commits_by_year[yy]
                        item['commits'] = commits
                        item['year'] = yy
                        MOOSEActivityYear(**item)
 
                    #year_month表
                    for info in MOOSEActivityYearMonth.select(MOOSEActivityYearMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                         
                    for yymm in reversed(sorted(data.commits_by_month.keys())):
                        item['commits'] = data.commits_by_month[yymm]
                        item['yearmonth'] = yymm
                        MOOSEActivityYearMonth(**item)
                     
                    #timezone表
                    for info in MOOSEActivityTimezone.select(MOOSEActivityTimezone.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item=dict()
                    item['oss_id'] = oss_info.oss_id;
                         
                    for i in sorted(data.commits_by_timezone.keys(), key = lambda n : int(n)):
                        item['commits'] = data.commits_by_timezone[i]
                        item['timezone'] = i                                                                                                    
                        MOOSEActivityTimezone(**item)                  
                        
                    #Author
                    #list
                    for info in MOOSEAuthorList.select(MOOSEAuthorList.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()   
                    item['oss_id'] = oss_info.oss_id;
                    count=0                     
                    for author in data.getAuthors(conf['max_authors']):
                        info = data.getAuthorInfo(author)
                        item['user_id'] = user_id[count]
                        count+=1
                        item['author'] = author
                        item['commits'] = info['commits']
                        item['commits_frac'] = '%.2f%%'%info['commits_frac']
                        item['lines_added'] = info['lines_added']
                        item['lines_removed'] = info['lines_removed']
                        item['first_commit'] = info['date_first']
                        item['last_commit'] = info['date_last']
                        item['age'] = str(info['timedelta'])
                        item['active_days'] = len(info['active_days'])
                        item['by_commits'] = info['place_by_commits']
                        MOOSEAuthorList(**item)
 
                   
                    #cumulated commits and lines
                    for info in MOOSEAuthorCumulated.select(MOOSEAuthorCumulated.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    lines_by_authors={}
                    commits_by_authors = {}
                    authors_to_plot = data.getAuthors(conf['max_authors'])
                    for author in authors_to_plot:
                        lines_by_authors[author] = 0
                        commits_by_authors[author] = 0
                    for stamp in sorted(data.changes_by_date_by_author.keys()):
                        item ['date'] = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')
                        for author in authors_to_plot:
                            if author in data.changes_by_date_by_author[stamp].keys():
                                lines_by_authors[author] = data.changes_by_date_by_author[stamp][author]['lines_added']
                                commits_by_authors[author] = data.changes_by_date_by_author[stamp][author]['commits']
                                item['author'] = author
                                item['cumulated_commits'] = commits_by_authors[author]
                                item['cumulated_lines'] = lines_by_authors[author]
                                MOOSEAuthorCumulated(**item)
                    
                    #month(author)表
                    for info in MOOSEAuthorMonth.select(MOOSEAuthorMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yymm in reversed(sorted(data.author_of_month.keys())):
                        authordict = data.author_of_month[yymm]
                        authors = getkeyssortedbyvalues(authordict)
                        authors.reverse()
                        commits = int(data.author_of_month[yymm][authors[0]])
                        next = ', '.join(authors[1:conf['authors_top']+1])
                        item['month'] = yymm
                        item['author'] = authors[0]
                        item['commits'] = '%d (%.2f%% of %d)'%( commits, (100.0 * commits) / data.commits_by_month[yymm], data.commits_by_month[yymm])
                        item['next_top5'] = ', '.join(authors[1:conf['authors_top']+1])
                        item['author_number'] = len(authors)
                        MOOSEAuthorMonth(**item)       
                    
                    #year(author)表
                    for info in MOOSEAuthorYear.select(MOOSEAuthorYear.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yy in reversed(sorted(data.author_of_year.keys())):
                        authordict = data.author_of_year[yy]
                        authors = getkeyssortedbyvalues(authordict)
                        authors.reverse()
                        commits = int(data.author_of_year[yy][authors[0]])
                        next = ', '.join(authors[1:conf['authors_top']+1])
                        item['year'] = yy
                        item['author'] = authors[0]
                        item['commits'] = '%d (%.2f%% of %d)'%( commits, (100.0 * commits) / data.commits_by_year[yy], data.commits_by_year[yy])
                        item['next_top5'] = ', '.join(authors[1:conf['authors_top']+1])
                        item['author_number'] = len(authors)
                        MOOSEAuthorYear(**item)                        
                    
                    #domains表
                    for info in MOOSEDomain.select(MOOSEDomain.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    domains_by_commits = getkeyssortedbyvaluekey(data.domains, 'commits')
                    domains_by_commits.reverse() # most first
                    n=0
                    for domain in domains_by_commits:
                        if n == conf['max_domains']:
                            break
                        commits = 0
                        n += 1
                        info = data.getDomainInfo(domain)
                        item['domain'] = domain
                        item['commits'] = int(info['commits'])
                        item['commits_frac'] = '%.2f%%'%((100.0 * info['commits'] /  data.getTotalCommits()))

                        MOOSEDomain(**item)
                    
                    #files
                    #count by date
                    for info in MOOSEFileDateCount.select(MOOSEFileDateCount.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for stamp in sorted(data.files_by_stamp.keys()):
                        item['date'] = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')
                        item['files'] = data.files_by_stamp[stamp]
                        MOOSEFileDateCount(**item)
                     
                    #extension
                    for info in MOOSEFileExtension.select(MOOSEFileExtension.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for ext in sorted(data.extensions.keys()):
                        files = data.extensions[ext]['files']
                        lines = data.extensions[ext]['lines']
                        try:
                            loc_percentage = (100.0 * lines) / data.getTotalLOC()
                        except ZeroDivisionError:
                            loc_percentage = 0
                        item['extension'] = ext
                        item['files'] = '%d (%.2f%%)'%(files, (100.0 * files) / data.getTotalFiles())
                        item['line'] = '%d (%.2f%%)'%(lines, loc_percentage)
                        item['filesdividelines'] = int (lines / files)
                            
                        MOOSEFileExtension(**item)
                     
                    #lines
                    #lines count by date
                    for info in MOOSELineDateCount.select(MOOSELineDateCount.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for stamp in sorted(data.changes_by_date.keys()):
                        item['date'] = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')
                        item['line'] = data.changes_by_date[stamp]['lines']
                        MOOSELineDateCount(**item)
                     
                    #tag
                    for info in MOOSETag.select(MOOSETag.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    tags_sorted_by_date_desc = list(map(lambda el : el[1], reversed(sorted(list(map(lambda el : (el[1]['date'], el[0]), data.tags.items()))))))                     
                    for tag in tags_sorted_by_date_desc:
                        authorinfo = []
                        authors_by_commits = getkeyssortedbyvalues(data.tags[tag]['authors'])
                        for i in reversed( authors_by_commits):
                            authorinfo.append('%s (%d)' % (i, data.tags[tag]['authors'][i]))
                        item['name'] = tag
                        item['date'] = data.tags[tag]['date']
                        item['commits'] = int(data.tags[tag]['commits'])
                        item['authors'] = ', '.join(authorinfo)
                        MOOSETag(**item)
                     
                
                        
                        
                except BaseException as ex:
                    print(ex)
                    pass
                finally:
                    os.chdir(prevdir)
              
     