from model.oss import *
from model.community import *
from model.user import *
import requests
import traceback
from multiprocessing import Process
from multiprocessing import queues
from multiprocessing.managers import BaseManager
import multiprocessing
import threading
import queue
import json


def get_nav_list(uid, cid):
    extra_info = dict()
    community = MOOSECommunity.objects.filter(user_id=int(uid))
    current_community = MOOSECommunity.objects.filter(id=int(cid))
    if current_community is not None and len(current_community) > 0:
        current_community_name = current_community[0].community_name
    else:
        current_community_name = ''
    community_list = MOOSECommunityList.objects.filter(community_id__in=community)
    extra_info.__setitem__('community', community)
    extra_info.__setitem__('community_list', community_list)
    user = MOOSEAdmin.objects.get(id=uid)
    extra_info.__setitem__('user', user)
    extra_info.__setitem__('cid', int(cid))
    extra_info.__setitem__('current_community_name', current_community_name)
    return extra_info

def get_html_text(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        if r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
        return r.text
    except:
        traceback.print_exc()


def get_html_json(url, header):
    try:
        response = requests.get(url, headers=header)
        text_info = response.text
        text_json = json.loads(text_info)
        head_info = response.headers
        return text_json, head_info
    except:
        traceback.print_exc()


def get_graphql(url, query, header):
    try:
        response = requests.post(url, json={'query': query}, headers=header)
        text_info = response.text
        text_json = json.loads(text_info)
        head_info = response.headers
        return text_json, head_info
    except:
        traceback.print_exc()

class QueueManager(BaseManager): pass


task_queue = queue.Queue()


def return_task_queue():
    global task_queue
    return task_queue


def get_thread_task_queue(queue_name):
    QueueManager.register(queue_name, callable=return_task_queue)
    manager = QueueManager(address=('127.0.0.1', 34512), authkey=b'abc')
    manager.start()
    return manager
