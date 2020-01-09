from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics
from django.views import View
from serializers import Serializer
import json

from model import user


def md5(user):
    import hashlib
    import time

    # 当前时间，相当于生成一个随机的字符串
    ctime = str(time.time())

    # token加密
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    def get(self, request, format=None):
        ret = {'code': 1000, 'msg': 'success', 'name': '偷偷'}
        ret = json.dumps(ret, ensure_ascii=False)
        return Response(ret)
        #return HttpResponse(ret)

    def post(self, request, format=None):
        data = request.data
        ret = {'code': 1000, 'msg': None}
        #user = request.POST.get('username')
        print(data['username'])

        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            obj = user.UserInfo.objects.filter(username=user).first()
            print(user)
            if not obj:
                # 如果用户第一次登陆则创建用户
                obj = user.UserInfo.objects.create(username=user, password=pwd)
                ret['code'] = 1001
                ret['msg'] = '创建用户成功'

            # 为用户创建token
            token = md5(user)
            # 存在就更新，不存在就创建
            user.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'
        
        return JsonResponse(ret)