#!/usr/bin/env python
# -*- codinfg:utf-8 -*-
'''
@author: Jeff LEE
@file: runner.py
@time: 2018-10-09 9:15
@desc:
'''
import os,sys,time
import unittest

from utils.HTMLTestRunner import HTMLTestRunner

#添加项目工程路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_case import baidu
from utils.baseEmail import Email

PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )

if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    # 定义个报告存放路径，支持相对路径
    report = PATH(r'../reports/'+now+'_'+'Report.html')

    with open(report, 'wb') as f:
        testunit = unittest.TestSuite()
        # 将测试用例加入到测试容器(套件)中
        testunit.addTest(unittest.makeSuite(baidu.TestBaiDu))
        runner = HTMLTestRunner(f, verbosity=2, title='百度自动化测试报告--uniquefu', description='百度自动化测试报告')
        runner.run(testunit)

    email=Email(report)
    email.send()
