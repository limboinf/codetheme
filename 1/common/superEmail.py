#coding=utf-8
"""
==================================
function:   基于新浪SAE邮件通用类
addDate:    2014-07-25
author:     BeginMan
==================================
"""
from sae.mail import EmailMessage, send_mail

class superMail(object):
    def __init__(self, emails, subject, html, smtp=''):
        self.emails = emails    # 邮箱列表
        self.subject = subject  # 邮件的标题
        self.html = html        # 正文
        self.smtp = ("smtp.vampire.com", 25, "codetheme@vampire.com", "1111", False)
        if smtp:
            self.smtp = smtp        # (smtp主机，smtp端口， 邮件地址或用户名，密码，是否启用TLS）

    def sendEmail(self):
        if self.emails:
            try:
                send_mail(self.emails, self.subject, self.html,self.smtp)
                return True
            except:
                return False
        return False

def tests():
    send_mail('xinxinyu2011@163.com', 'test', 'ts',
              ("smtp.gmail.com", 25, "pythonsuper@gmail.com", "fang1991", True)
    )

