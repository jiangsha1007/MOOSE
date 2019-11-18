# -*- coding: utf8 -*-
from model.common_model import *
from core.common_git import *
from core.datacollector import *
from core.common import *
from apscheduler.schedulers.background import BlockingScheduler
import datetime

# 代码分析
class CodeAnalysis:
    def __init__(self):
        manager = get_thread_task_queue('getcoude_queue')
        self.task_queue = manager.getcoude_queue()

    # 获取代码
    def get_code(self):
        
        sched = BlockingScheduler(timezone='MST')
        #表示从周一到周五9点30分10秒更新
        #sched.add_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10')
        sched.add_job(self.get_code_true, 'interval',  seconds=300)
        sched.start()
 
            
         
     
    def  get_code_true(self):
        print ("new")
        for i in range(3):
            p = multiprocessing.Process(target=self._get_code_process, args=(self.task_queue, i,))
            p.start()
        oss_info = OsslibMetadata_2.select(OsslibMetadata_2.q.oss_git_url != "")

        for per_oss_info in oss_info:
            print ("acting")
            if per_oss_info.oss_git_url != '':
                trans_info = []
                trans_info.append(per_oss_info.oss_name)
                trans_info.append(per_oss_info.oss_git_url)
                trans_info.append(per_oss_info.oss_git_tool)
                trans_info.append(per_oss_info.id)
                self.task_queue.put(trans_info)
        p.join()


    @staticmethod
    def _get_code_process(q, i):
        time1=time.clock()
        while True:
            if q.empty():
                print ('waiting')
                time.sleep(3)
                time2=time.clock()
                if time2-time1 >= 5:
                    break
                continue
            info = q.get()
            oss_name = info[0]
            oss_git_url = info[1]
            oss_git_tool = info[2]
            oss_id = info[3]
            return_info = -1
            print (oss_id)
        
            if oss_git_tool == 'Git':
                return_info = get_repo_by_git('data/'+oss_name,oss_git_url)#'git://git.code.sf.net' 
            elif oss_git_tool == 'SVN':
                return_info = get_repo_by_svn('data/' + oss_name, 'https://svn.code.sf.net' + oss_git_url)
            if return_info == 1:
                oss_info = OsslibMetadata_2.get(oss_id)
                oss_info.oss_local_path = 'data/' + oss_name
            
            time1=time.clock()
           
          

    def code_analysis(self):
        format = '%Y-%m-%d %H:%M:%S'
        Year = int(datetime.datetime.now().strftime(format)[:4])
        weekdays = ['mon','tue','wed','thu','fri','sat','sun']
        months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
       
        
         
        for oss_info in OsslibMetadata_2.select(OsslibMetadata_2.q.id == '45808'):

            prevdir = os.getcwd()
            users=OsslibDeveloper.select(OsslibDeveloper.q.oss_id == oss_info.oss_id)
            sorted(users,key = lambda user :user.user_commit_count)
            user_id=[]
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
                    
                    #General表
                    for info in OsslibGeneral.select(OsslibGeneral.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)                                        
                    item=dict()
                    item['oss_id'] = oss_info.oss_id;
                    item['project_name'] =  data.projectname
                    item['generated'] = '%s (in %d seconds)'%(datetime.datetime.now().strftime(format), time.time() - data.getStampCreated())
                    item['generator'] = 'GitStats  (version %s), %s ' % (getversion(), getgitversion() )
                    item['report_period'] =  ' %s to %s ' % (data.getFirstCommitDate().strftime(format), data.getLastCommitDate().strftime(format))
                    item['age_days'] =  '%d days, %d active days (%3.2f%%) ' % (data.getCommitDeltaDays(), len(data.getActiveDays()), (100.0 * len(data.getActiveDays()) / data.getCommitDeltaDays()))
                    item['total_files'] =  '%d' % (data.getTotalFiles())
                    item['total_lines_of_code'] =  'Lines of Code %s (%d added, %d removed)' % (data.getTotalLOC(), data.total_lines_added, data.total_lines_removed)
                    item['total_commits'] =  ' %s (average %.1f commits per active day, %.1f per all days) ' % (data.getTotalCommits(), float(data.getTotalCommits()) / len(data.getActiveDays()), float(data.getTotalCommits()) / data.getCommitDeltaDays())
                    item['authors'] =  '%s (average %.1f commits per author) ' % (data.getTotalAuthors(), (1.0 * data.getTotalCommits()) / data.getTotalAuthors())
                    OsslibGeneral(**item)
                     
                    #Activity
                    #32week表
                    for info in OsslibActivityWeek.select(OsslibActivityWeek.q.oss_id == oss_info.oss_id):
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
                            OsslibActivityWeek(**item)
                 
                
                    #24hour表
                    for info in OsslibActivityHour.select(OsslibActivityHour.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    hour_of_day = data.getActivityByHourOfDay()
                    for i in range(0,24):
                        if i in hour_of_day:
                            item['commits'] = hour_of_day[i]
                            item['hour'] = i
                            OsslibActivityHour(**item)
                     
                    #7day表
                    for info in OsslibActivityDay.select(OsslibActivityDay.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    day_of_week = data.getActivityByDayOfWeek()
                    for i in range(0,7):
                        if i in day_of_week:
                            item['commits'] = day_of_week[i]
                            item['day'] = weekdays[i]
                            OsslibActivityDay(**item)
                        
               
                    #hour_week表
                    for info in OsslibActivityHourOfWeek.select(OsslibActivityHourOfWeek.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for weekday in range(0, 7):
                        for hour in range(0, 24):
                            try:
                                commits = data.activity_by_hour_of_week[weekday][hour]
                                item['commits'] = commits
                                item['weekday_hour'] = '%s_%d'%(weekdays[weekday],hour)                                 
                                OsslibActivityHourOfWeek(**item)
                            except KeyError:
                                pass
                  
                    
                    #month表
                    for info in OsslibActivityMonth.select(OsslibActivityMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for mm in range(1, 13):
                        if mm in data.activity_by_month_of_year:
                            commits = data.activity_by_month_of_year[mm]
                            item['commits'] = commits
                            item['month'] = months[mm-1]
                            OsslibActivityMonth(**item) 
               
                    #year表
                    for info in OsslibActivityYear.select(OsslibActivityYear.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yy in reversed(sorted(data.commits_by_year.keys())): 
                        commits = data.commits_by_year[yy]
                        item['commits'] = commits
                        item['year'] = yy
                        OsslibActivityYear(**item)
 
                    #year_month表
                    for info in OsslibActivityYearMonth.select(OsslibActivityYearMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                         
                    for yymm in reversed(sorted(data.commits_by_month.keys())):
                        item['commits'] = data.commits_by_month[yymm]
                        item['yearmonth'] = yymm
                        OsslibActivityYearMonth(**item)
                     
                    #timezone表
                    for info in OsslibActivityTimezone.select(OsslibActivityTimezone.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item=dict()
                    item['oss_id'] = oss_info.oss_id;
                         
                    for i in sorted(data.commits_by_timezone.keys(), key = lambda n : int(n)):
                        item['commits'] = data.commits_by_timezone[i]
                        item['timezone'] = i                                                                                                    
                        OsslibActivityTimezone(**item)                  
                        
                    #Author
                    #list
                    for info in OsslibAuthorList.select(OsslibAuthorList.q.oss_id == oss_info.oss_id):
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
                        OsslibAuthorList(**item)
 
                   
                    #cumulated commits and lines
                    for info in OsslibAuthorCumulated.select(OsslibAuthorCumulated.q.oss_id == oss_info.oss_id):
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
                                OsslibAuthorCumulated(**item)
                    
                    #month(author)表
                    for info in OsslibAuthorMonth.select(OsslibAuthorMonth.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yymm in reversed(sorted(data.author_of_month.keys())):
                        authordict = data.author_of_month[yymm]
                        authors = getkeyssortedbyvalues(authordict)
                        authors.reverse()
                        commits = data.author_of_month[yymm][authors[0]]
                        next = ', '.join(authors[1:conf['authors_top']+1])
                        item['month'] = yymm
                        item['author'] = authors[0]
                        item['commits'] = '%d (%.2f%% of %d)'%( commits, (100.0 * commits) / data.commits_by_month[yymm], data.commits_by_month[yymm])
                        item['next_top5'] = ', '.join(authors[1:conf['authors_top']+1])
                        item['author_number'] = len(authors)
                        OsslibAuthorMonth(**item)       
                    
                    #year(author)表
                    for info in OsslibAuthorYear.select(OsslibAuthorYear.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for yy in reversed(sorted(data.author_of_year.keys())):
                        authordict = data.author_of_year[yy]
                        authors = getkeyssortedbyvalues(authordict)
                        authors.reverse()
                        commits = data.author_of_year[yy][authors[0]]
                        next = ', '.join(authors[1:conf['authors_top']+1])
                        item['year'] = yy
                        item['author'] = authors[0]
                        item['commits'] = '%d (%.2f%% of %d)'%( commits, (100.0 * commits) / data.commits_by_year[yy], data.commits_by_year[yy])
                        item['next_top5'] = ', '.join(authors[1:conf['authors_top']+1])
                        item['author_number'] = len(authors)
                        OsslibAuthorYear(**item)                        
                    
                    #domains表
                    for info in OsslibDomain.select(OsslibDomain.q.oss_id == oss_info.oss_id):
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
                        item['commits'] = '%d (%.2f%%)'%(info['commits'], (100.0 * info['commits'] /  data.getTotalCommits()))
                        OsslibDomain(**item)
                    
                    #files
                    #count by date
                    for info in OsslibFileDateCount.select(OsslibFileDateCount.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for stamp in sorted(data.files_by_stamp.keys()):
                        item['date'] = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')
                        item['files'] = data.files_by_stamp[stamp]
                        OsslibFileDateCount(**item)
                     
                    #extension
                    for info in OsslibFileExtension.select(OsslibFileExtension.q.oss_id == oss_info.oss_id):
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
                            
                        OsslibFileExtension(**item)
                     
                    #lines
                    #lines count by date
                    for info in OsslibLineDateCount.select(OsslibLineDateCount.q.oss_id == oss_info.oss_id):
                        info.delete(info.id)
                    item = dict()
                    item['oss_id'] = oss_info.oss_id;
                    for stamp in sorted(data.changes_by_date.keys()):
                        item['date'] = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d')
                        item['line'] = data.changes_by_date[stamp]['lines']
                        OsslibLineDateCount(**item)
                     
                    #tag
                    for info in OsslibTag.select(OsslibTag.q.oss_id == oss_info.oss_id):
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
                        item['commits'] = data.tags[tag]['commits']
                        item['authors'] = ', '.join(authorinfo)
                        OsslibTag(**item)
                     
                
                        
                        
                except BaseException as ex:
                    print(ex)
                    pass
                finally:
                    os.chdir(prevdir)
              
     