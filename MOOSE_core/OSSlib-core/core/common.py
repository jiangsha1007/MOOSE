import requests
import traceback
from multiprocessing import Process
from multiprocessing import queues
from multiprocessing.managers import BaseManager
import multiprocessing
import threading
import queue
import json


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


class DictManager(BaseManager): pass


task_queue = queue.Queue()
task_dict = dict()


def return_task_queue():
    global task_queue
    return task_queue


def return_task_dict():
    global task_dict
    return task_dict

def get_thread_task_queue(queue_name):
    QueueManager.register(queue_name, callable=return_task_queue)
    manager = QueueManager(address=('127.0.0.1', 34512), authkey=b'abc')
    manager.start()
    return manager


def get_thread_task_dict(dict_name):
    DictManager.register(dict_name, callable=return_task_dict)
    manager = DictManager(address=('127.0.0.1', 34513), authkey=b'bcd')
    manager.start()
    return manager

