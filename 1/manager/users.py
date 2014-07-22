# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from common import ajax
from common.superqiniu import SuperQiniu
from manager.models import MyUser
from mysite.models import Signal, LoveUser
from common.form import AdminSignalForm, PasswordForm, AvatarForm
from django.db.models import Q

def userSuccess(request, id):
    """用户注册成功跳转页面"""
    context = {}
    context['id'] = id
    return render(request, 'manager/user/user_success.html', context)



def userInfo(request, id):
    """用户信息"""
    context = {}
    user = request.user
    is_owner, loved = 0, 0

    if user.is_authenticated and user.id == int(id):
        is_owner = 1
        user_ = user
    else:
        user_ = MyUser.objects.get(pk=id)
    if user.is_authenticated and LoveUser.objects.filter(user=user, who=id).exists():
        loved = 1       # 是否关注了他
    context['is_owner'] = is_owner
    context['loved'] = loved
    context['id'] = id
    context['us'] = user_
    return render(request, 'manager/user/user.html', context)



def changeUserInfo(request):
    """修改用户"""
    import re
    RESERVED_WORDS = [
    'root', 'admin', 'bot', 'robot', 'master', 'webmaster',
    'account', 'people', 'user', 'users', 'project', 'projects',
    'search', 'action', 'favorite', 'like', 'love', 'none',
    'team', 'teams', 'group', 'groups', 'organization',
    'organizations', 'package', 'packages', 'org', 'com', 'net',
    'help', 'doc', 'docs', 'document', 'documentation', 'blog',
    'bbs', 'forum', 'forums', 'static', 'assets', 'repository',
    u'傻逼', u'牛逼', u'二逼', u'2b'
    'public', 'private',
    'mac', 'windows', 'ios', 'lab',
    ]

    if request.method == 'POST':
        user = request.user
        data = request.POST.get('obj', '').strip()
        type = int(request.POST.get('type'))
        if type == 0:   # 更改用户名
            if data and len(data) > 20 and len(data) < 3:
                return ajax.ajax_ok(u'用户名不能超过20个字符,不小于3个字符')
            if data in RESERVED_WORDS:
                return ajax.ajax_ok(u'该名称太特殊，已禁用')
            if MyUser.objects.filter(username=data).exists() and user.username != data:
                return ajax.ajax_ok(u'用户名已被注册')
            user.username = data
            user.save()

        if type == 1:   # 更改邮箱
            if data and len(data) < 7 and not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", data):
                return ajax.ajax_ok(u'邮箱格式不对')
            if MyUser.objects.filter(email=data).exists() and user.email != data:
                return ajax.ajax_ok(u'该邮箱已存在')
            user.email = data
            user.save()
        if type == 2:   # 更改性别
            sex = 1 if data == u'男' else 0
            user.sex = sex
            user.save()
        if type == 3:   # 更改站点
            user.url = data
            user.save()
        if type == 4:
            if len(data) > 1000:
                return ajax.ajax_ok(u'字数太多了……')
            user.desc = data
            user.save()
        return ajax.ajax_ok(u'修改成功')


def changePwd(request):
    """更改密码"""
    context = {}
    user = request.user
    context['form'] = PasswordForm()
    if request.method == 'POST':
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            newpwd = form.cleaned_data.get('password1', None)
            if newpwd:
                user.set_password(newpwd)
                user.save()
                return HttpResponseRedirect('/manage/success/?url=%s' % str(request.path))

        context['form'] = form
    return render(request, 'manager/user/pwd.html', context)


def setAvatar(request):
    """更改头像"""
    context = {}
    user = request.user
    context['form'] = AvatarForm()
    context['pic'] = ['/site_media/avatar/%s.jpg' % str(i) for i in range(1, 36)]
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = request.FILES['avatar']
            qiniu = SuperQiniu(avatar)            # 实例化超级七牛类
            qiniu.uploadFile()                    # 上传文件
            url = qiniu.downloadFile()              # 返回url
            user.avatar = url
            user.save()
            # return HttpResponseRedirect('/manage/success/?url=%s' % str(request.path))
        context['form'] = form
    return render(request, 'manager/user/avatar.html', context)



def choice_avatar(request):
    """选择头像"""
    if request.method == 'POST':
        url = request.POST.get('url')
        user = request.user
        user.avatar = url
        user.save()
        return HttpResponse('ok')



def sendMs(request):
    """管理员发布公告"""
    context = {}
    if request.method == 'POST':
        user = request.user
        f = AdminSignalForm(request.POST)
        fobj = f.save(commit=False)
        fobj.user = user
        fobj.save()
        return HttpResponseRedirect('/')
    f = AdminSignalForm()
    context['form'] = f
    return render(request, 'manager/user/adminSendMs.html', context)


def getMs(request):
    """获取消息列表"""
    context = {}
    user = request.user

    sys_signal = Signal.objects.filter(who=0, status__lt=2).order_by('status', '-id')  # 所有消息
    list_id = Signal.objects.filter(who=user.id, type=0).values_list('obj', flat=True)
    for i in sys_signal:
        if i.id not in list_id:
            Signal.objects.create(who=user.id, user=i.user, title=i.title, content=i.content, obj=i.id)

    signal = Signal.objects.filter(who=user.id, status__lt=2).order_by('status', '-id')  # 所有消息
    context['signal'] = signal

    return render(request, 'manager/user/signal.html', context)



def delMs(request):
    """删除消息"""
    if request.method == 'POST':
        id = request.POST.get('id')
        Signal.objects.filter(id=id).update(status=2)
        return ajax.ajax_ok()



def readMs(request):
    """标记消息未已读"""
    if request.method == 'POST':
        id = request.POST.get('m_id')
        Signal.objects.filter(id=id).update(status=1)
        return ajax.ajax_ok(id)
