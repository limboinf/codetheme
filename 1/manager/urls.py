# coding=utf-8
from django.conf.urls import patterns, include, url

# Theme
urlpatterns = patterns('manager.views',
    url(r'^$', 'manage', name='manage'),                            # 后台首页
    url(r'^success/$', 'success', name='success'),                  # 所有操作成功跳转页面
    url(r'^addtheme/$', 'addtheme', name='addtheme'),               # 发布编程主题
    url(r'^addcode/$', 'addcode', name='addcode'),                  # 保存分类
    url(r'^addtag/$', 'addtag', name='addtag'),                     # 保存标签
    url(r'^themeManage/$', 'themeManage', name='themeManage'),      # theme Manage.
    url(r'^theme/del/$', 'deltheme', name='deltheme'),              # 删除主题
    url(r'^theme/list/$', 'themeList', name='themeList'),           # theme list.
    url(r'^theme/(?P<id>\d+)/$', 'themeView', name='themeView'),    # 主题详情
    url(r'^theme/changeSchedule/$', 'changeSchedule', name='changeSchedule'),    # 更改主题进度
)

#user
urlpatterns += patterns('manager.users',
    url(r'^user/(?P<id>\d+)/$', 'userInfo', name='userInfo'),       # 用户信息
    url(r'^user/pwd/$', 'changePwd', name='changePwd'),             # 修改密码
    url(r'^user/set_avatar/$', 'setAvatar', name='setAvatar'),             # 修改头像
    url(r'^user/choice_avatar/$', 'choice_avatar', name='choice_avatar'),   # 选择头像
    url('^user/change_userinfo/$', 'changeUserInfo', name='changeUserInfo'),        # 修改用户
    url('^user/ms/$', 'getMs', name='getMs'),                       # 获取消息
    url('^user/ms/read/$', 'readMs', name='readMs'),                       # 标记消息为已读
    url('^user/del_ms/$', 'delMs', name='delMs'),                   # 删除消息
    url(r'^user/admin/sendMs/$', 'sendMs', name='sindms'),          # 管理员发布公告
)

#share
urlpatterns += patterns('manager.myshare',
    url(r'^share/add/$', 'add', name='add'),          # 发布
    url(r'^share/list/$', 'list', name='share_list'),          # 链接列表
    url(r'^share/del/$', 'shareDel', name='share_del'),          # 链接列表
)

#admin
urlpatterns += patterns('manager.super',
    url(r'^admin/$', 'superAdmin', name='superAdmin'),          # 管理员主页
    url(r'^admin/type/$', 'type', name='type'),                 # 分类管理
    url(r'^admin/msg/$', 'msg', name='msg'),                    # 公告管理
    url(r'^admin/user/$', 'users', name='users'),               # 用户管理
    url(r'^admin/top/$', 'tops', name='tops'),                  # 帖子管理
)

# common 通用
urlpatterns += patterns('manager.common',
    url(r'^common/add/$', 'add', name='add'),                          # 公共添加
    url(r'^common/del/$', 'del_', name='del_'),                         # 公共删除
    url(r'^common/update/$', 'update', name='update'),                    # 公共更新
)
