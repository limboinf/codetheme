# coding=utf-8
from django.conf.urls import patterns, include, url
from django.views.decorators.cache import cache_page

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.home', name='home'),                   # 首页
    url(r'^about/$', 'mysite.views.about', name='about'),                   # 首页
    url(r'^share/', include('share.urls')),                         # share
    url(r'^manage/', include('manager.urls')),                      # manager
    url(r'^admin/', include(admin.site.urls)),                      # admin
)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
   (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)

# Theme
urlpatterns += patterns('mysite.views',
    url(r'^login/$', 'login_', name='login'),                           # 登陆
    url(r'^login/weibo/$', 'weiboLogin', name='weiboLogin'),            # 登陆
    url(r'^logout/$', 'logout_', name='logout'),                        # 登出
    url(r'^login/weibo_check/$', 'weibo_check', name='weibo_check'),     # 微博回调地址
    url(r'^register/$', 'register', name='register'),                   # 注册

    url(r'^codetheme/(?P<id>\d+)/$', 'codetheme', name='codetheme'),      # 详细页
    url(r'^codetheme/love/$', 'love', name='love'),                      # 关注与取消
    url(r'^codetheme/get_user_info/$', 'get_user_info', name='get_user_info'), # 个人用户信息
    url(r'^codetheme/get_user_recent/$', 'get_user_recent', name='get_user_recent'), # 个人用户信息
    url(r'^codetheme/get_hot_theme/$', 'get_hot_theme', name='get_hot_theme'), # 个人用户信息
    url(r'^codetheme/get_recent_share/$', 'get_recent_share', name='get_recent_share'), # 个人用户信息

    url(r'^codetheme/hot/$', 'hot', name='hot'), # 最热主题
    url(r'^codetheme/user/list/', 'userList', name='userList'),     # 会员列表
    url(r'^codetheme/get_user_status/$', 'getUserStatus', name='getUserStatus'),  # 获取用户主题，分享，关注人，fans
    url(r'^codetheme/loveuser/$', 'loveuser', name='loveuser'),     # 关注某人

    url(r'^codetheme/sendms/$', 'sendms', name='sendms'),   # 发送私信
    url(r'^codetheme/lovedtheme/$', 'lovedtheme', name='lovedtheme'),   # 我关注的主题
    url(r'^codetheme/type/(?P<id>\d+)/$', 'searchType', name='searchType'),   # 相关类型的主题
    url(r'^codetheme/tag/(?P<id>\d+)/$', 'searchTag', name='searchTag'),   # 相关类型的主题
    url(r'^codetheme/comment/$', 'comment', name='comment'),        # 主题评论
    url(r'^codetheme/feedback/$', 'feedback', name='feedback'),        # 反馈
)
