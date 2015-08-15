# -*- coding:utf-8 -*-
import urllib2
import requests


class Client(object):
    """
        一个用来访问网络资源的客户端
        可以重写以定制你需要的客户端类型
    """
    def __init__(self,name='default_client'):
        self.name = name

    def get(self, url, data):
        """ 发送请求url，data参数是一个字典,返回相应正文 """
        response = requests.get(url, data)
        return response.content