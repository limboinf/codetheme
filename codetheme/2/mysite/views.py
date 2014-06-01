# coding=utf-8
from django.shortcuts import render
from mysite.form import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from share.models import Code, Tag, Theme, Node
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
    return render(request, 'login.html', context)


def logout_(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def manage(request):
    """后台"""
    context = {}
    return render(request, 'manage.html', context)


@login_required(login_url='/login/')
def addtheme(request):
    """发布编程主题"""
    context = {}
    user = request.user
    if request.method == 'POST':
        pass
    else:
        codes = Code.objects.filter(user=user.id)
        tags = Tag.objects.filter(user=user.id).order_by('-id')
        context['codes'] = codes
        context['tags'] = tags
    return render(request, 'addtheme.html', context)


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
    if request.method == 'POST':
        tags = request.POST.get('tags', '')
        if tags:
            tag = json.dumps(tags)
        if not Code.objects.filter(name__iexact=code).exists():
            c_id = Code.objects.create(user=user.id, name=code).id
            return ajax.ajax_ok(c_id)



