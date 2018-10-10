#!/usr/bin/env python
# -*- codinfg:utf-8 -*-
'''
@author: Jeff LEE
@file: a.py
@time: 2018-10-09 11:34
@desc:
'''
# !/usr/bin/env python -u
# -*- coding:utf-8 -*-
import time
import unittest
import sys
from utils.HTMLTestRunner import HTMLTestRunner
from datetime import datetime
from time import sleep


class LoginAndroidTests(unittest.TestCase):

    def test_a(self):
        print(u"\n测试开启！当前测试次数：")
        print(u"\n测试开启时间：")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(u"\n测试结束！成功次数:")
        print(u"\n测试结束时间：")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':
    test_unit = unittest.TestSuite()
    test_unit.addTest(LoginAndroidTests("test_a"))
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    fp = open(now + "result.html", 'wb')
    runner = HTMLTestRunner(stream=fp, title=u"测试报告", description=u"测试结果详情：")
    runner.run(test_unit)
    fp.close()