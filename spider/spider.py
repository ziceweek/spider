# -*- coding:utf-8 -*-
import gevent
from gevent import monkey; monkey.patch_all()
from bs4 import BeautifulSoup
import multiprocessing
from util.message import Message

from config.config import queue_todo,queue_responses,queue_results,coroutine_num,myclient


# 请求url,将响应写入队列 urf->response
def _fetch(message_urf):
    """
    :param message_urf: Message对象，_name='urf'
    :return: 成功返回True
    """
    try:
        message_urf.set('response', myclient.get(message_urf.get('url')))
        if not message_urf.has('data'):
            message_urf.set('data', {})
        queue_responses.put(message_urf.to_json())
        return True
    except Exception,what:
        print what
        return False


# 从todo任务队列中返回n个 message_urf
def _pull_urfs(n, timeout=1):
    """
    :param n: 每次取的条数
    :param timeout: 取队列时，超时时间
    :return: 一个Message列表
    """
    message_urfs = []
    for i in range(0, n):
        if len(message_urfs) == 0:
            m = queue_todo.get(block=True)
        else:
            m = queue_todo.get(block=True, timeout=timeout)
            if m is None:
                return message_urfs

        m = Message(name='urf')
        m.parse_json(m)
        message_urfs.append(m)
    return message_urfs


def todo(url='',func='',data={}):
    queue_todo.put(Message(name='urf',url=url, func=func,data=data).to_json())

# 下载器，处理todo队列中的内容，每一个请求一个协程
def downloader(n=coroutine_num):
    """
    使用gevent实现，异步下载器
    :param n: 一次开启的下载个数
    :return:
    """
    while True:
        threads = [gevent.spawn(_fetch, u) for u in _pull_urfs(n)]
        gevent.joinall(threads)


# html内容提取 处理response中的内容
def extractor():
    """
    对内容进行解析提取
    :return:
    """
    while True:
        m = Message(name='urf').parse_json(queue_responses.get())
        handler(m['url'], m['response'], m['func'], m['data'])  # response是由请求url返回来的


# 指定函数处理某个链接
def handler(url, response, func_name, data):
    """ 调用函数 func_name(url,response,data) """
    eval(func_name)(url, response, data)


# url处理函数
def a(url, response, data):
    f = open('html/'+url+'.html', 'w')
    f.write(response)
    f.close()
    print url
    soup = BeautifulSoup(response)
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        todo(url=a_tag['href'], func='a')



if __name__ == "__main__":

    todo(url='http://finance.sina.com.cn/',func='a')

    process2 = multiprocessing.Process(target=extractor)
    process1 = multiprocessing.Process(target=downloader)

    # jobs = []
    # jobs.append(process1)
    # jobs.append(process2)
    process1.start()
    process2.start()

    process1.join()
    process2.join()




