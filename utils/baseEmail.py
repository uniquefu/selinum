#!/usr/bin/env python
# -*- codinfg:utf-8 -*-
'''
@author: Jeff LEE
@file: baseEmail.py
@time: 2018-07-16 14:19
@desc:邮件类。用来给指定用户发送邮件。可指定多个收件人，可带附件。
'''
import re,os,time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error

from utils.file_reader import yamlReader

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

a= PATH('../conf/conf.yaml')

email =yamlReader(a).data
email_data=email['email']

class Email(object):
    def __init__(self, path=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = email_data['title']
        self.message = email_data['message']
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = email_data['server']
        self.sender = email_data['sender']
        self.receiver = email_data['receiver']
        self.password = email_data['password']

    def _attach_file(self, att_file):
        """将单个文件添加到附件列表中"""
        att = MIMEText(open('%s' % att_file, 'rb').read(), 'plain', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        att["Content-Disposition"] = 'attachment; filename="%s"' % file_name[-1]
        self.msg.attach(att)
        # logger.info('attach file {}'.format(att_file))

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = ','.join(self.receiver)  # 多个显示的收件人

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 添加附件，支持多个附件（传入list），或者单个附件（传入str）
        if self.files:
            if isinstance(self.files, list):
                for f in self.files:
                    self._attach_file(f)
            elif isinstance(self.files, str):
                self._attach_file(self.files)

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP('smtp.126.com','25')  # 连接sever
        except (gaierror and error) as e:
            pass
            # logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                pass
                # logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver, self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接
                # logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            # '同时检查收件人地址是否正确'.format(self.title, self.receiver))
# t =time.strftime('%Y%m%d%H%M%S', time.localtime())
# report = [PATH('../reports/Report.xlsx'),PATH('../reports/Report.html')]
# email = Email(title='CamTalk测试报告--%s' %t,
#                message='这是今天的测试报告，请查收！',
#                receiver='164234020@qq.com',
#                server=('smtp.126.com', '25'),
#                sender='uniquefu@126.com',
#                password='lg162200100',
#                path=report
#                )