# -*- coding:utf-8 -*-
import json
# import logging
# from redisQueue import RedisQueue


class Message:

    def __init__(self, name='defulat_Message',**args):
        """
        :param name: 消息的名称
        :param args: 作为消息的内容，一些键值对
        """
        self.name = name
        self.dict = {
            '_name':name,
        }
        for arg in args:
            self.dict[arg] = args[arg]

    def set(self, key, value):
        """ 设置键值对 """
        self.dict[str(key)] = value

    def get(self, key):
        """ 获取键key对应的值 """
        if key in self.dict:
            return self.dict[key]
        else:
            raise BaseException('Message:'+self.name+' has not key "'+key+'".')

    def __getitem__(self, key):
        """ 获取键key对应的值 """
        if key in self.dict:
            return self.dict[key]
        else:
            raise BaseException('Message:'+self.name+' has not key "'+key+'".')

    def has(self, key):
        if key in self.dict:
            return True
        else:
            return False

    def to_json(self):
        """ 转化为json输出 """
        return json.dumps(self.dict)

    def parse_json(self, json_str):
        """ 载入json，并解析，其中的键会覆盖Message中的同名键 """
        try:
            d = json.loads(json_str)
            for key in d:
                self.dict[key] = d[key]
        except Exception, what:
            print what


#
# rq = RedisQueue('result')
# msg = Message()
# msg.set('url','http://www.redis.cn/commands.html')
# msg.set('urls',['/commands/hexists.html','http://www.baidu.com'])
# rq.put(msg.to_json())

