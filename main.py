__author__ = 'zice'
from spider.spider import extractor,downloader,todo
import multiprocessing

if __name__ == "__main__":

    todo(url='http://finance.sina.com.cn/',func='a')

    process2 = multiprocessing.Process(target=extractor)
    process1 = multiprocessing.Process(target=downloader)

    process1.start()
    process2.start()

    process1.join()
    process2.join()