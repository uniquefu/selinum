#!/usr/bin/env python
# -*- codinfg:utf-8 -*-
'''
@author: Jeff LEE
@file: logs.py
@time: 2018-07-31 9:17
@desc:
'''

import time,os
import logging, logging.handlers

#使用相对路径+绝对路径
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
log_path = PATH("../log")
print(log_path)
path=log_path+'/mylog.log'
now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
png = log_path+'/'+now+'error_png.png'

class Logger(object):
    def __init__(self, path=path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        #fh = logging.FileHandler(path)

        '''
        TimedRotatingFileHandler构造函数声明
        class logging.handlers.TimedRotatingFileHandler(filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None)
        filename    日志文件名前缀
        when        日志名变更时间单位
            'S' Seconds
            'M' Minutes
            'H' Hours
            'D' Days
            'W0'-'W6' Weekday (0=Monday)
            'midnight' Roll over at midnight
        interval    间隔时间，是指等待N个when单位的时间后，自动重建文件
        backupCount 保留日志最大文件数，超过限制，删除最先创建的文件；默认值0，表示不限制。
        delay       延迟文件创建，直到第一次调用emit()方法创建日志文件
        atTime      在指定的时间（datetime.time格式）创建日志文件。
        '''

        fh = logging.handlers.TimedRotatingFileHandler(path, when='D', interval=1, backupCount=0)
        # 设置日志文件后缀，以当前时间作为日志文件后缀名。
        #fh.suffix = "%Y%m%d%H%M%S.log"
        fh.suffix = "%Y%m%d%H%M%S.log"
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)

        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warn(message)

    def error(self, driver,message):
        driver.get_screenshot_as_file(png)
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def startLine(self,cls_name,message):
        self.logger.info('***************** %s  %s  START ********************'%(cls_name,message))

    def endLine(self,cls_name,message):
        self.logger.info('***************** %s %s  END ********************'%(cls_name,message))

logger=Logger()

