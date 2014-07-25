# coding=utf-8
from django.shortcuts import render
from common.form import LoginForm, RegisterForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from mysite.models import Type, Tag, Theme, Signal, Love, LoveUser, ThemeTag, Comment
from django.conf import settings
from manager.models import MyUser
from share.models import Share
from common import ajax
from common.superEmail import superMail
from common.sqldata import SelectAllSqlByColumns
from common.superweibo import SupserWeibo
import simplejson as json
from django.views.decorators.cache import cache_page
from weibo import APIClient
import datetime
from django.shortcuts import get_object_or_404
from django.core.cache import cache

def home(request):
    """网站首页."""
    context = {}
    user = request.user
    is_active = True
    if user.is_authenticated():
        is_active = False
    # 编程主题
    themes = Theme.objects.all().order_by('-id')
    context['themes'] = themes
    context['is_active'] = is_active
    return render(request, 'index.html', context)


def login_(request):
    """登陆"""
    context = {}
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()      # 获取用户实例
            if user:
                login(request, user)
                if form.get_auto_login():       # set session
                    request.session.set_expiry(None)
                if form.get_user_is_first():     # 判断用户是否首次登录
                    user_id = form.get_user_id()
                    return HttpResponseRedirect('/manage/user/%s/' % user_id)
                return HttpResponseRedirect('/')
        context['form'] = form

    else:
        form = LoginForm()
        context['form'] = form
    return render(request, 'theme/login.html', context)


def weiboLogin(request):
    """微博登录"""
    client = APIClient(app_key=settings.APP_KEY, app_secret=settings.APP_SERCET, redirect_uri=settings.CALLBACK_URL)
    url = client.get_authorize_url()
    return HttpResponseRedirect(url)


def weibo_check(request):
    code = request.GET.get('code', None)
    now = datetime.datetime.now()
    if code:
        client = APIClient(app_key=settings.APP_KEY, app_secret=settings.APP_SERCET, redirect_uri=settings.CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token   # 返回的token，类似abc123xyz456
        expires_in = r.expires_in       # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
        uid = r.uid
        # 在此可保存access token
        client.set_access_token(access_token, expires_in)
        request.session['access_token'] = access_token
        request.session['expires_in'] = expires_in
        request.session['uid'] = uid
        user = SupserWeibo(access_token=access_token, uid=uid, request=request)      # 实例化超级微博类
        # 更新数据库
        if MyUser.objects.filter(uid=uid).exists():
            MyUser.objects.filter(uid=uid).update(last_login=now)
            user.Login()    # 登陆
            return HttpResponseRedirect('/')
        else:
            # 创建用户并登陆
            u_id = user.createUser()
            if u_id:
                return HttpResponseRedirect('/manage/user/%s/' %u_id)
    return HttpResponse('/404/')


def logout_(request):
    """退出"""
    logout(request)
    return HttpResponseRedirect('/')



def register(request):
    """注册"""
    context = {}
    if request.method == 'POST':
        form = RegisterForm(request, request.POST)
        if form.is_valid():
            email = list(form.get_email())
            # 发送邮件激活
            subject = u'Python研究社邮箱验证'
            html = '<p>Welcome!</p>'
            s = superMail(email)
            if s.sendEmail():
                return HttpResponseRedirect('/')

        context['form'] = form
    else:
        context['form'] = RegisterForm()
    return render(request, 'theme/register.html', context)


def about(request):
    """关于"""
    return render(request, 'about.html')



def codetheme(request, id=None):
    """详细页面"""
    context = {}
    theme = Theme.objects.get(pk=id)
    theme.counts += 1
    theme.save()
    context['theme'] = theme

    if request.method == 'GET':
        context['form'] = CommentForm()
    else:
        form = CommentForm(request, request.POST)
        if form.is_valid():
            return HttpResponseRedirect(str(request.path))
        context['form'] = form
    return render(request, 'theme/theme.html', context)


def love(request):
    """关注"""
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id')
        type = request.POST.get('type')
        theme = get_object_or_404(Theme, pk=int(id))
        # 自身不能关注自身
        if not Theme.objects.filter(id=id, user=user.id).exists():
            if type == '0'and Love.objects.filter(theme__id=id, user=user).exists():
                Love.objects.filter(theme__id=id, user=user).delete()
            elif not Love.objects.filter(theme__id=id, user=user).exists():
                Love.objects.create(theme_id=id, user=user)
                Signal.objects.create(type=4, obj=id, user=user, who=theme.user)

        return HttpResponse('ok')


@cache_page(60 * 60)
def get_user_info(request):
    """user info"""
    if request.method == 'POST':
        context = {}
        user = request.user
        context['mylove'] = Love.objects.filter(user=user).count()      # 我关注的主题
        context['theme'] = Theme.objects.filter(user=user.id).count()   # 我发布的主题
        context['youlove'] =LoveUser.objects.filter(user=user).count()  # 我关注的人
        context['loveyou'] = LoveUser.objects.filter(who=user.id).count()  # 谁关注的我
        context['share'] = Share.objects.filter(user=user.id).count()   # 我发布的链接
        return render(request, 'common/user_info.html', context)

@cache_page(60 * 60)
def get_user_recent(request):
    """最近加入的用户"""
    if request.method == 'POST':
        context = {}
        context['recent_user'] = MyUser.objects.filter(is_active=1)[:10]
        return render(request, 'common/user_recent.html', context)


@cache_page(60 * 60)
def get_hot_theme(request):
    """精华主题"""
    if request.method == 'POST':
        context = {}
        # 月热门主题
        day = datetime.datetime.now()
        hottheme = getMonthHotTheme()[:10] if len(getMonthHotTheme())>10 else getMonthHotTheme()
        context['hottheme'] = hottheme
        context['month'] = day.month
        return render(request, 'common/hot_theme.html', context)


@cache_page(60 * 30)
def get_recent_share(request):
    """最近加入的用户"""
    if request.method == 'POST':
        context = {}
        context['share'] = Share.objects.all().order_by('-id').values('id', 'title', 'url')[:10]
        return render(request, 'common/recent_share.html', context)



def hot(request):
    """精华主题"""
    context = {}
    context['themes'] = getMonthHotTheme()
    return render(request, 'theme/hot.html', context)


def userList(request):
    """会员列表"""
    context = {}
    sql = """
    select x.*, count(y.user) from (
    select u.id,u.username,u.url,u.desc,u.avatar,count(t.user) from user u
    left join theme t on t.user=u.id
    group by t.user
    ) x left join share y on y.user=x.id
    group by y.user
    """
    context['users'] = SelectAllSqlByColumns(sql, ['id', 'username', 'url', 'desc', 'avatar', 'countTheme', 'countShare'])
    return render(request, 'theme/userlist.html', context)



def getMonthHotTheme():
    """获取月份精华主题"""
    if cache.get('hotTheme', None):
        return cache.get('hotTheme')

    day = datetime.datetime.now()
    sql = """
    select t.id,u.username,u.id,u.avatar,t.title,t.counts,count(l.id) as star,t.summary, ty.name as tyname, ty.id as tyid from theme t
    inner join user u on u.id = t.user
    inner join type ty on ty.id = t.type
    left join love l on l.theme_id=t.id
    where t.end_date between '%s' and '%s'
    group by t.id order by star desc, counts desc
    """ %("%s-%s-01" % (day.year, day.month), "%s-%s-30" % (day.year, day.month))
    hottheme = SelectAllSqlByColumns(sql, ['id', 'username', 'u_id','avatar', 'title', 'counts', 'star', 'summary', 'tyname', 'tyid'])
    cache.set('hotTheme', hottheme, 60*60*10)
    return hottheme


def getUserStatus(request):
    """获取用户信息，主题，分享，关注人,fans"""
    if request.method == 'POST':
        context = {}
        uid = request.POST.get('uid')
        type = int(request.POST.get('type', 1))
        context['type'] = type
        if type == 1:       # 主题
            context['theme'] = Theme.objects.filter(user=uid)
        if type == 2:       # 分享
            context['share'] = Share.objects.filter(user=uid)
        if type == 3:       # 关注的人
            context['us'] = LoveUser.objects.filter(user__id=uid)
        if type == 4:       # fans
            context['fans'] = LoveUser.objects.filter(who=uid)
        return render(request, 'theme/getuserstatus.html', context)


def loveuser(request):
    """关注"""
    if request.method == 'POST':
        uid = request.POST.get('uid')
        type = int(request.POST.get('type', 1))
        user = request.user
        if type == 1 and not LoveUser.objects.filter(who=uid, user=user).exists():
            LoveUser.objects.create(who=uid, user=user)
            Signal.objects.create(type=3, obj=0, user=user, who=uid)

        else:
            LoveUser.objects.filter(who=uid, user=user).delete()
        return HttpResponse('ok')


def sendms(request):
    """发送私信"""
    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title', '')
        who = request.POST.get('who')
        content = request.POST.get('content', '')
        Signal.objects.create(type=2, obj=0, user=user, who=who, title=title, content=content)
        # 发邮件
        return HttpResponse('ok')


def lovedtheme(request):
    """我关注的主题"""
    context = {}
    user = request.user
    context['themes'] = Love.objects.filter(user=user).order_by('-id')
    return render(request, 'theme/lovedtheme.html', context)


def searchType(request, id=None):
    """相关类型的主题"""
    context = {}
    if id:
        context['type'] = id
        context['typename'] = Type.objects.get(pk=id).name
        context['themes'] = Theme.objects.filter(type=id).order_by('-id')
        return render(request, 'theme/type_theme.html', context)

    return HttpResponseRedirect('/404/')


def searchTag(request, id=None):
    """相关类型的主题"""
    context = {}
    if id:
        context['tag'] = ThemeTag.objects.get(pk=id).tag.id
        context['tagname'] = ThemeTag.objects.get(pk=id).tag.name
        context['themes'] = ThemeTag.objects.filter(tag__id=id).order_by('-id')
        return render(request, 'theme/tag_theme.html', context)

    return HttpResponseRedirect('/404/')


def comment(request):
    """加载评论"""
    if request.method == 'POST':
        context = {}
        id = request.POST.get('id')
        context['comments'] = Comment.objects.filter(type=1, obj=id).order_by('add_date')
        context['counts'] = len(context['comments'])
        return render(request, 'theme/comment.html', context)


def feedback(request):
    """反馈"""
    return render(request, 'theme/feedback.html')