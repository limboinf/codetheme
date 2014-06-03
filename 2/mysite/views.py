# coding=utf-8
from django.shortcuts import render
from mysite.form import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from share.models import Code, Tag, Theme, Node, Share
from mysite import ajax
import simplejson as json

def home(request):
    """index."""
    context = {}
    return render(request, 'index.html', context)


def login_(request):
    """登陆"""
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            us = form.cleaned_data.get('us')
            pwd = form.cleaned_data.get('pwd')
            auto_login = form.cleaned_data.get('auto_login', None)
            user = authenticate(username=us, password=pwd)
            if user and user.is_active:
                login(request, user)
                if auto_login:       # set session
                    request.session.set_expiry(None)
                return HttpResponseRedirect('/manage/')

    else:
        form = LoginForm()
    context['form'] = form
    return render(request, 'manage/login.html', context)


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def manage(request):
    """后台"""
    context = {}
    user = request.user
    #codetheme
    themes = Theme.objects.filter(user=user.id).order_by('-id')
    print themes
    share = Share.objects.filter(user=user.id).order_by('-id')
    context['themes'] = themes
    context['share'] = share
    return render(request, 'manage/manage.html', context)


@login_required(login_url='/login/')
def addtheme(request):
    """发布编程主题"""
    context = {}
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        code = request.POST.get('code')
        desc = request.POST.get('desc', '')
        tags = request.POST.get('tags', '')
        begin_date = request.POST.get('begin_date')
        end_date = request.POST.get('end_date')
        map = request.POST.get('map', '')       # 思维导图
        code = Code.objects.get(pk=code)
        if tags:
            tags = json.loads(tags)
            str_tags = []
            for i in tags:
                i = i.strip()
                if i:
                    str_tags.append(i)
                if i and not Tag.objects.filter(name__iexact=i).exists():
                    Tag.objects.create(name=i, user=user.id)

            str_tags = json.dumps(str_tags)

        if map:
            pass

        Theme.objects.create(
            title=title,
            user=user.id,
            type=code,
            tag=str_tags,
            content=desc,
            start_date=begin_date,
            end_date=end_date
        )
        return ajax.ajax_ok()
    else:
        codes = Code.objects.filter(user=user.id)
        tags = Tag.objects.filter(user=user.id).order_by('-id')
        context['codes'] = codes
        context['tags'] = tags
    return render(request, 'manage/addtheme.html', context)


@login_required(login_url='/login/')
def addcode(request):
    """添加分类"""
    user = request.user
    if request.method == 'POST':
        code = request.POST.get('code').strip().lower()
        if not Code.objects.filter(name__iexact=code).exists():
            c_id = Code.objects.create(user=user.id, name=code).id
            return ajax.ajax_ok(c_id)


@login_required(login_url='/login/')
def addtag(request):
    """添加标签"""
    user = request.user



@login_required(login_url='/login/')
def themeManage(request):
    """Theme Manage"""
    context = {}
    user = request.user
    context['codes'] = Code.objects.filter(user=user.id)
    context['tags'] = Tag.objects.filter(user=user.id).order_by('-id')
    return render(request, 'manage/thememanage.html', context)



@login_required(login_url='/login/')
def themeList(request):
    """Theme list"""
    context = {}
    user = request.user
    if request.method == 'POST':
        themes = Theme.objects.filter(user=user.id)
        code = int(request.POST.get('code', 0))
        tags = int(request.POST.get('tag', 0))
        status = int(request.POST.get('status', 3))
        title = request.POST.get('title', '')
        if code:
            themes = themes.filter(type=code)
        if status != 3:
            themes = themes.filter(status=status)
        if title:
            themes = themes.filter(title__iexact=title)
        if tags:
            tagName = Tag.objects.get(pk=tags).name
            for i in themes:
                if tagName not in json.loads(i.tag):
                    themes.filter(id=i.id)


        context['themes'] = themes.order_by('-id')
        return render(request, 'manage/themeList.html', context)



@login_required(login_url='/login/')
def themeView(request, id=None):
    """Theme manage view."""
    context = {}
    user = request.user
    if id:
        theme = Theme.objects.get(pk=id)
        context['themes'] = theme
        return render(request, 'manage/themeview.html', context)


@login_required(login_url='/login/')
def deltheme(request):
    """删除主题"""
    if request.method == 'POST':
        id = request.POST.get('id')
        Theme.objects.filter(id=id).delete()
        return ajax.ajax_ok()