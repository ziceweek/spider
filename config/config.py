# -*- coding:utf-8 -*-
import redisQueue,noRepeatRedisQueue
from util.client import Client
from Queue import Queue

# queue
queue_todo = noRepeatRedisQueue.RedisQueue('todo_test',host='localhost',port=6379,db=0)  # url func_name处理 uf
queue_results = redisQueue.RedisQueue('results_test',host='localhost',port=6379,db=0)
queue_responses = redisQueue.RedisQueue('response_test',host='localhost',port=6379,db=0)  # 由url 得到的response 由func_name处理 urf

# # queue
# queue_todo = Queue()  # url func_name处理 uf
# queue_results = Queue()
# queue_responses = Queue()  # 由url 得到的response 由func_name处理 urf

# 用于下载的协程数
coroutine_num = 100

# 客户端
myclient = Client(name='myClient')

