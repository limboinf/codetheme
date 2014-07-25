#coding=utf-8
import random
import string
import re
from manager.models import MyUser

#生成l位随机密码
def GenPassword(l):
    chars=string.letters+string.digits
    return ''.join([random.choice(chars) for i in range(l)])


#URLz正则
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def ValidUs(username):
    """验证用户名是否存在"""
    if MyUser.objects.filter(username=username).exists():
        return ValidUs(username+GenPassword(2))
    else:
        return username

