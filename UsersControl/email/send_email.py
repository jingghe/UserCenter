#-*- coding: utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import logging
from UserCenter import settings
logger = logging.getLogger('django_log_file')


class SendEmail(object):

    def __init__(self, *args, **kwargs):

        self.Sender_user = getattr(settings, 'MAIL_USER')
        self.Sender_password = getattr(settings, 'MAIL_PASS')
        self.Mail_host = getattr(settings, 'MAIL_HOST')
        self.Mail_port = getattr(settings, 'MAIL_PORT')

        self.Receiver_user = kwargs['Receiver_user']
        self.Receiver_password = kwargs['Receiver_pass']
        self.Nickname = kwargs['Receiver_nikname']
        self.username = kwargs['username']
        self.first_templet =  """
                <h1><font color='red'>Gaea 用户中心账户开通成功</font></h1>
                <h3>您好:<font color='red'>%s</font></h3>
                <p>          Gaea 用户中心账户权限已经开通,账户和密码如下:</p>
                <p>账户:<font color='red'>%s</font></p>
                <p>密码:<font color='red'>%s</font></p>
                登陆跳板机ip:192.168.7.191  端口:21987
                <h3><a>初次登陆，请点击</a><a href=http://www.baidu.com><font 
                color='blue'>%s/Modify/Pass/</font></a><a>修改密码</a></h3>
                <font color='blue'>Gaea 用户中心账户问题或者需求请联系运维部运维工程师:</font><font color='red'>赵虹 
                联系邮箱地址:zhaohong@globalegrow.com</font><br /><br />
                <h3><font color='red'>该邮件，请忽回复,谢谢!</font><br /><br /><h3>
        """ % (self.Nickname, self.username, self.Receiver_password,  self.Receiver_user)

        self.reset_templet = """
                <h1><font color='red'>Gaea 用户中心账户密码重置成功</font></h1>
                <h3>您好:<font color='red'>%s</font></h3>
                <p>          Gaea 用户中心账户密码已经重置,账户和密码如下:</p>
                <p>账户:<font color='red'>%s</font></p>
                <p>密码:<font color='red'>%s</font></p>
                <h3><a>你可以点击</a><a href=http://www.baidu.com><font 
                color='blue'>%s/Modify/Pass/</font></a><a>修改密码</a></h3>
                <font color='blue'>Gaea 用户中心账户问题或者需求请联系运维部运维工程师:</font><font color='red'>赵虹 
                联系邮箱地址:zhaohong@globalegrow.com</font><br /><br />
                <h3><font color='red'>该邮件，请忽回复,谢谢!</font><br /><br /><h3>
        """ % (self.Nickname, self.username, self.Receiver_password, self.Receiver_user)

    def send(self, first=None):
        try:
            msg = MIMEMultipart()
            if first:
                templet = self.first_templet
                msg["Subject"] = "LDAP系统账户开通(重要)"
            else:
                templet = self.reset_templet
                msg["Subject"] = "LDAP系统账户密码重置(重要)"
            send_obj = MIMEText(templet, "html", 'utf-8')
            send_obj["Accept-Language"] = "zh-CN"
            send_obj["Accept-Charset"] = "ISO-8859-1,utf-8"
            msg.attach(send_obj)
            msg["From"] = self.Sender_user
            msg["To"] = self.Receiver_user
            s = smtplib.SMTP()
            s.connect(self.Mail_host, self.Mail_port)
            s.login(self.Sender_user, self.Sender_password)
            s.sendmail(self.Sender_user, [self.Receiver_user, ], msg.as_string())
            s.quit()
            return True
        except smtplib.SMTPException as e:
            print u'无法发送邮件',e
            logger.error('无法发送邮件',e)
            return False