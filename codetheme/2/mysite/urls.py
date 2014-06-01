from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mysite.views.home', name='home'),                   #　首页
    url(r'^login/$', 'mysite.views.login_', name='login'),          # 登陆
    url(r'^logout/$', 'mysite.views.logout_', name='logout'),       # 登出
    url(r'^manage/$', 'mysite.views.manage', name='manage'),        # 后台首页
    url(r'^manage/addtheme/$', 'mysite.views.addtheme', name='addtheme'),#发布编程主题
    url(r'^manage/addcode/$', 'mysite.views.addcode', name='addtheme'),     # 保存分类
    url(r'^manage/addtag/$', 'mysite.views.addtag', name='addtag'),     # 保存标签
    url(r'^manage/addnode/$', 'mysite.views.addnode', name='addnode'),  # 保存学习思路

    url(r'^share/', include('share.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

# Serve static files for admin, use this for debug usage only
# `python manage.py collectstatic` is preferred.
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('',
   (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}), 
)
