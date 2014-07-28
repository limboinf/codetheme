#coding=utf-8
"""
==================================
function:   基于新浪SAE邮件通用类
addDate:    2014-07-25
author:     BeginMan
==================================
"""
# from sae.mail import EmailMessage, send_mail
from django.core.mail import EmailMultiAlternatives

class superMail(object):
    def __init__(self, emails, subject, html, form_email='xinxinyu2011@163.com'):
        self.emails = emails    # 邮箱LIST列表
        self.subject = subject  # 邮件的标题
        self.html = html        # 正文
        self.form_email = form_email


    def sendEmail(self):
        try:
            text_content = 'Python研究社发来的邮件'
            msg = EmailMultiAlternatives(self.subject, text_content, self.form_email, self.emails)
            msg.attach_alternative(self.html, 'text/html')
            msg.send()
            return True
        except Exception, e:
            print e
            return False



