from git import Repo
import git
from apscheduler.schedulers.background import BlockingScheduler
#clone_repo = Repo.clone_from('https://github.com/5162/test', 'test/ts')
#remote=Repo.remote
local_path='test/ts'
def update():
    try:
        clone_repo = Repo.clone_from('https://github.com/5162/test', 'test/ts')
    except:
        remote = git.repo.base.Repo(local_path).remote()# 从远程版本库拉取分支
        remote.pull('master') #后面跟需要拉取的分支名称
        print ('onetime')
 
sched = BlockingScheduler(timezone='MST')
sched.add_job(update, 'interval',  seconds=10)
sched.start()
 