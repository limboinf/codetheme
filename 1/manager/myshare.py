# coding=utf-8
from django.shortcuts import render
from common.form import ShareForm
from django.http import HttpResponseRedirect, HttpResponse
from mysite.models import Type, Tag, Theme, ThemeTag
from share.models import Share
from django.conf import settings
from common import ajax
from common.sqldata import SelectAllSqlByColumns
from common.superweibo import SupserWeibo
import simplejson as json
from weibo import APIClient


def add(request):
    """添加"""
    context = {}
    user = request.user
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = user.id
            f.save()
            return HttpResponseRedirect('/manage/share/list/')
        context['form'] = form
    else:
        form =  ShareForm()
        context['form'] = form
    return render(request, 'manager/share/add.html', context)



def list(request):
    """个人分享列表."""
    context = {}
    user = request.user

    title = request.GET.get('title', '')
    share = Share.objects.filter(user=user.id)
    if title:
        share = share.filter(title__contains=title)

    context['share'] = share
    return render(request, 'manager/share/list.html', context)


def shareDel(request):
    """删除"""
    if request.method == 'POST':
        id = request.POST.get('id')
        Share.objects.filter(id=id).delete()
        return ajax.ajax_ok()