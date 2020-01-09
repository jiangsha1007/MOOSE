from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time
import os
def task():
    # 你的spider启动命令
    subprocess.Popen('scrapy crawl MOOSE')
    pass

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # 每20分钟执行一次
    scheduler.add_job(task, 'cron', minute="*/1")
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()