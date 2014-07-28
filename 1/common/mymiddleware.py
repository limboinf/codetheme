#coding=utf-8
#中间件扩展
__author__ = 'beginman'
from mysite.models import Signal
from manager.models import MyUser
from django.http import HttpResponseRedirect

LOGIN_URLS = ['/manage/']
ADMIN_URLS = ['/manage/user/admin/sendMs/']
ANONYMOUS_URLS = ['/manage/userGreat/']

class Mymiddleware(object):
    def process_request(self, request):
        """Request预处理函数"""
        path = str(request.path)
        if path.startswith('/site_media/'):
            return None
        #验证登陆
        if request.user.is_anonymous():
            for obj in ANONYMOUS_URLS:
                if path.startswith(obj):
                    return None

            for obj in LOGIN_URLS:
                if path.startswith(obj):
                    return HttpResponseRedirect('/login/?url=%s' % path)

        #管理员通道验证
        if not request.user.is_anonymous():
            if not request.user.is_admin:
                for obj in ADMIN_URLS:
                    if path.startswith(obj):
                        return HttpResponseRedirect('/404/')
        # 信息提醒
        user = request.user
        if user.is_authenticated():
            if user.type == -1 and not path.startswith('/account/tip/') and not path.startswith('/logout/'):
                return HttpResponseRedirect('/account/tip/')

            signal = Signal.objects.filter(who=user.id, status=0).count()   # 所有未读消息
            signal_obj_list = Signal.objects.filter(who=user.id, type=0).values_list('obj', flat=True)
            sys_signal_list = Signal.objects.filter(who=0, status=0).values_list('id', flat=True)  # 所有系统消息
            sys_signal_list = [i for i in sys_signal_list if i not in signal_obj_list]
            request.session['ms'] = signal+len(sys_signal_list)
            return None

