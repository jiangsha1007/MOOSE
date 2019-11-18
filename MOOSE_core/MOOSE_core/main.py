from model.common_model import *
from multiprocessing.managers import BaseManager
from scrapy import cmdline
from apscheduler.schedulers.background import BlockingScheduler
from multiprocessing import Process
import queue
from core.statistics import *
 
 
from core.code_analysis import *
 
 

task_queue = queue.Queue()
 
def run():
    cmdline.execute("scrapy crawl repos".split())

def processrun():
    p = Process(target=run,)
    p.start()
    p.join()

    
 
def read_file(q, i):
    while(True):
        pass

def return_task_queue():
    global task_queue
    return task_queue
class QueueManager(BaseManager): pass


if __name__ == '__main__':
    #conclude_similar()
    # 通过多个社区api获取repo列表,
    osslib_community_list = OsslibCommunityApi.select()
    '''
    for per_software_community in osslib_community_list:
       eval(per_software_community.community_name)().get_oss_list(2)
    '''
    CodeAnalysis().get_code()
    CodeAnalysis().code_analysis()

    #train()
 
        
    sched = BlockingScheduler(timezone='MST')
    #表示从周一到周五9点30分10秒更新
    #sched.add_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10')
    #sched.add_job(processrun, 'interval',  seconds=500)
    #sched.add_job(CodeAnalysis().process, 'interval', seconds=1)
    Statistics().oss_stat()
    sched.start()
    



    '''
    all_json_file = list(path.glob('**/*.json'))
    QueueManager.register('get_task_queue', callable=return_task_queue)
    manager = QueueManager(address=('127.0.0.1', 34512), authkey=b'abc')
    manager.start()
    task = manager.get_task_queue()
    for json_file in all_json_file:
        task.put(json_file)
    for i in range(50):
        p = multiprocessing.Process(target=read_file, args=(task,i,))
        p.start()
    p.join()
    '''
#github_event_watch(repo_id=1,event_id=1,event_payload='1',event_time='1',update_time='1',user_id=1,org_id=1,event_public=1)