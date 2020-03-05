from django.shortcuts import render
import threading
from dwebsocket.decorators import accept_websocket
import time
from view.overview import *
# 连接websocket  ws://localhost：8000/websocketLink/22
# 因为 websocket 是协议  所以不能用 http或https
clients = []
@accept_websocket
def websocketLink(request):
    while 1:
        if not request.is_websocket():
            try:
                message = request.GET['message']
                return HttpResponse(message)
            except:
                return render(request, 'index.html')
        else:
            data = get_overview_data(15)
            print(data)
            request.websocket.send(json.dumps(data))
            time.sleep(3)

 # 发送消息
def websocketMsg(client, msg):
    import json
    # 因为一个账号会有多个页面打开 所以连接信息需要遍历
    for cli in client:
        'client客户端 ，msg消息'
        b1 = json.dumps(msg).encode('utf-8')
        client[cli].send(b1)


# 服务端发送消息
def send(username, title, data, url):
    'username:用户名 title：消息标题 data：消息内容，消息内容:ulr'
    try:
        if clients[username]:
            websocketMsg(clients[username], {'title': title, 'data': data, 'url': url})
            # 根据业务需求 可有可无    数据做 持久化
            # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=0)

            flg = 1
        flg = -1
    except BaseException:
        # messageLog = MessageLog(name=username, msg_title=title, msg=data, msg_url=url, is_required=1)
        pass
    finally:
        pass
# messageLog.save()