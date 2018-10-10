#!/usr/bin/env python
# -*- codinfg:utf-8 -*-
'''
@author: Jeff LEE
@file: test_baidu.py
@time: 2018-07-06 14:07
'''
import time,os
import unittest

from  selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from utils import HTMLTestRunner
from utils.logs import logger

import inspect


def get_current_function_name():
    return inspect.stack()[1][3]

class TestBaiDu(unittest.TestCase):
    '''百度'''
    def setUp(self):
        try:
            self.driver = webdriver.Firefox()
        except Exception as e:
            logger.error('打开浏览器失败'+e)

        # 添加智能等待
        self.driver.implicitly_wait(30)
        self.base_url = 'https://www.baidu.com/'


    def tearDown(self):
        self.driver.quit()
        pass

    def test_baidu_search(self):
        u'''百度搜索'''
        driver=self.driver
        logger.startLine(self.__class__.__name__ ,get_current_function_name())
        try:
            print('打开网页')
            driver.get(self.base_url)

            print('输入搜索内容')
            driver.find_element_by_id('kw').clear()
            driver.find_element_by_id('kw').send_keys('uniquefu')

            print('点击搜索')
            driver.find_element_by_id('su').click()
            time.sleep(3)

            print('检查点校验成功')

            logger.info(u'执行成功')
        except Exception as e:
            print('用例执行失败:' + repr(e))
            logger.error(driver,u'用例执行失败:'+repr(e))
            raise str(e)

        finally:
            logger.endLine(self.__class__.__name__ ,get_current_function_name())
            # logger.error('用例执行失败',e)

    def test_baidu_set(self):
        u'''百度设置'''
        driver = self.driver
        logger.startLine(self.__class__.__name__,get_current_function_name())
        try:
            print('打开网页')
            driver.get(self.base_url)

            # 进入搜索设置页面
            print('进入搜索设置页面')
            elment = driver.find_element_by_link_text('设置')
            ActionChains(driver).move_to_element(elment).perform()
            driver.find_element_by_link_text('搜索设置').click()
            time.sleep(3)

            # 修改设置
            print('修改设置')
            driver.find_element_by_id('s1_2').click()
            time.sleep(3)

            # 保存设置
            print('保存设置')
            driver.find_element_by_link_text('保存设置').click()
            time.sleep(3)

            # 获取网页上的警告信息并接收警告信息
            print('确认保存设置')
            alert = driver.switch_to_alert().accept()
            time.sleep(3)
            print('检查点校验成功')

            logger.info(u'执行成功')
        except Exception as e:
            logger.error(driver,u'用例执行失败:' + str(e))
            print(repr(e))
            raise e

        finally:
            logger.endLine(self.__class__.__name__ ,get_current_function_name())
            # logger.error('用例执行失败', e)

if __name__ == '__main__':
    PATH = lambda p: os.path.abspath(
        os.path.join(os.path.dirname(__file__), p)
    )

    # 定义个报告存放路径，支持相对路径
    report = PATH('Report.html')
    runner = unittest.TextTestRunner()
    with open(report, 'wb') as f:
        testunit = unittest.TestSuite()
        testunit.addTest(unittest.makeSuite(TestBaiDu))
        runner = HTMLTestRunner.HTMLTestRunner(f, verbosity=2, title='百度自动化测试报告--uniquefu', description='百度自动化测试报告')
        runner.run(testunit)
