# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.home', name='home'),                   # 首页
    url(r'^share/', include('share.urls')),
    url(r'^admin/', include(admin.site.urls)),
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
    url(r'^login/$', 'login_', name='login'),          # 登陆
    url(r'^logout/$', 'logout_', name='logout'),       # 登出
    url(r'^manage/$', 'manage', name='manage'),        # 后台首页
    url(r'^manage/addtheme/$', 'addtheme', name='addtheme'),# 发布编程主题
    url(r'^manage/addcode/$', 'addcode', name='addcode'),     # 保存分类
    url(r'^manage/addtag/$', 'addtag', name='addtag'),     # 保存标签
    url(r'^manage/addnode/$', 'addnode', name='addnode'),  # 保存学习思路
    url(r'^manage/themeManage/$', 'themeManage', name='themeManage'),  # theme Manage.
    url(r'^manage/theme/del/$', 'deltheme', name='deltheme'),  # 删除主题
    url(r'^manage/theme/(?P<id>\d+)/$', 'themeView', name='themeView'),  # 删除主题
)
