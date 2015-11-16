#coding=utf-8
"""
==================================
function:   基于新浪微博API，对微博登陆进行扩展
addDate:    2014-06-04
author:     BeginMan
==================================
"""

from django.conf import settings
import urllib
import urllib2
import simplejson as json
from manager.models import MyUser
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

import datetime
# 默认图片
DEFAULT_PIC = 'http://images.cnitblog.com/news/66372/201405/271116202595556.jpg'

# 用户信息
USER_INFO_URL = 'https://api.weibo.com/2/users/show.json'
# 发送微博
SEND_WEIBO_URL = 'https://api.weibo.com/2/statuses/upload_url_text.json'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0'
headers = {'User-Agent': user_agent}

class SupserWeibo(object):
    def __init__(self, access_token, uid, request=None, **kwargs):
        self.access_token = access_token
        self.uid = uid
        self.request = request
        self.user_cache = None
        self.kwargs = kwargs


    def createUser(self):
        """创建用户"""
        userInfo = self.getUserInfo()
        username=userInfo.get('screen_name')
        if MyUser.objects.filter(username=username).exists():
            username = username+'[weibo]'
        u_id = 0
        try:
            new_user = MyUser.objects.create_user(
                    email=str(self.uid) + '@weibo.com',
                    username=username,
                    password=self.uid,
                    type=1,
                    sex=int(userInfo.get('sex', 1)),
                    uid=self.uid,
                    access_token=self.access_token,
                    url=userInfo.get('url', ''),
                    desc =userInfo.get('description', ''),
                    avatar=userInfo.get('avatar_large')
            )
            u_id = new_user.id
        except:
            pass
        self.Login()    # 登陆
        return u_id

    def getUserInfo(self):
        """获取微博用户信息"""
        data = {'access_token': self.access_token, 'uid': self.uid}
        params = urllib.urlencode(data)
        values = urllib2.Request(USER_INFO_URL+'?%s' %params, headers=headers)
        response = urllib2.urlopen(values)
        result = json.loads(response.read())
        if result.get('error_code', None):
            # 写入日志
            print '获取用户信息失败'
            return False
        return result

    def SendWeibo(self):
        """用户发送微博"""
        status = self.kwargs.get('status', None)       # 微博内容
        visible = self.kwargs.get('visible', 0)     # 微博的可见性，0：所有人能看，1：仅自己可见，2：密友可见，3：指定分组可见，默认为0。
        url = self.kwargs.get('url', DEFAULT_PIC)   # 配图
        result = {}
        if status:
            data = {'access_token': self.access_token, 'status': status, 'visible':visible, 'url':url}
            params = urllib.urlencode(data)
            values = urllib2.Request(USER_INFO_URL+'?%s' %params, headers=headers)
            response = urllib2.urlopen(values)
            result = json.loads(response.read())
            if result.get('error_code', None):
                # 写入日志
                print '发送微博失败'
                return False
            return True
        return result

    def Login(self):
        """登陆"""
        user_ = MyUser.objects.filter(uid=self.uid)[0]
        user = authenticate(email=user_.email, password=self.uid)
        login(self.request, user)



