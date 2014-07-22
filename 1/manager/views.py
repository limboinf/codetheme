# coding=utf-8
from django.shortcuts import render
from common.form import LoginForm, RegisterForm, ThemeForm
from django.http import HttpResponseRedirect, HttpResponse
from mysite.models import Type, Tag, Theme, ThemeTag, Node, Love,Comment,Signal,ThemeUrl
from share.models import Share
from django.conf import settings
from django.shortcuts import get_object_or_404
from common import ajax
from common.page import get_page
from common.sqldata import SelectAllSqlByColumns
from common.superweibo import SupserWeibo
import simplejson as json
import datetime
from weibo import APIClient


def manage(request):
    """后台"""
    context = {}
    user = request.user
    #codetheme
    themes = Theme.objects.filter(user=user.id).order_by('-id')
    share = Share.objects.filter(user=user.id).order_by('-id')
    context['themes'] = themes
    context['share'] = share
    return render(request, 'manager/manage/manage.html', context)


def success(request):
    """所有成功跳转页面"""
    context = {}
    user = request.user
    path = request.get_full_path().split('=')
    req_path = '/'
    if len(path) == 2:
        req_path = path[1]
    context['req_path'] = req_path
    return render(request, 'manager/manage/success.html', context)


def addtheme(request):
    """发布编程主题"""
    context = {}
    now = datetime.datetime.now()
    user = request.user
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            title = formData.get('title')
            content = formData.get('content')
            type = formData.get('type')
            start_date = formData.get('start_date')
            end_date = formData.get('end_date')
            tags = request.POST.get('id_tag', '')
            obj = int(request.POST.get('edit_or_creat'))    # 编辑还是创建
            now = datetime.datetime.now()
            # 保存theme
            # 将markdown格式转换纯文本
            from BeautifulSoup import BeautifulSoup
            from markdown import markdown
            html = markdown(content)
            if len(content) > 500:
                html = markdown(content[:500])
            summary = ''.join(BeautifulSoup(html).findAll(text=True))
            if obj:     # 编辑状态
                theme = Theme.objects.get(id=obj)
                Theme.objects.filter(id=obj).update(title=title,type=int(type),summary=summary,content=content,start_date=start_date,end_date=end_date,add_date=now)
            else:
                theme = Theme.objects.create(
                    title=title,user=user.id,type=int(type),summary=summary,content=content,start_date=start_date,end_date=end_date, add_date=now
                )
            if tags:
                tags = json.loads(tags)
                tag_list = []
                for i in tags:
                    i = i.strip()
                    if i and not Tag.objects.filter(name__iexact=i).exists():
                        tag = Tag.objects.create(name=i, user=user.id)
                        tag_list.append(tag)
                    elif i:
                        tag_list.append(Tag.objects.filter(name__iexact=i)[0])

                # 创建ThemeTag
                for i in tag_list:
                    ThemeTag.objects.create(theme=theme, tag=i)
            return HttpResponseRedirect('/')

        context['form'] = form
        return render(request, 'manager/manage/addtheme.html', context)
    else:
        id = request.GET.get('id', None)
        context['form'] = ThemeForm()
        is_edit = 0
        if id:      # 编辑状况
            is_edit = id
            theme = get_object_or_404(Theme, pk=int(id))
            context['form'] = ThemeForm(instance=theme)
            context['has_tags'] = ThemeTag.objects.filter(theme__id=id)
        codes = Type.objects.filter(user=user.id)
        tags = Tag.objects.filter(user=user.id).order_by('-id')
        context['codes'] = codes
        context['tags'] = tags
        context['is_edit'] = is_edit
    return render(request, 'manager/manage/addtheme.html', context)


def addcode(request):
    """添加分类"""
    user = request.user
    if request.method == 'POST':
        code = request.POST.get('code').strip().lower()
        if not Type.objects.filter(name__iexact=code).exists():
            c_id = Type.objects.create(user=user.id, name=code).id
            return ajax.ajax_ok(c_id)


def addtag(request):
    """添加标签"""
    user = request.user



def themeManage(request):
    """主题管理页面"""
    context = {}
    user = request.user
    context['theme'] = 1 if Theme.objects.filter(user=user.id).exists() else 0
    context['codes'] = Type.objects.filter(user=user.id)
    context['tags'] = Tag.objects.filter(user=user.id).order_by('-id')
    return render(request, 'manager/manage/thememanage.html', context)



def themeList(request):
    """主题列表"""
    context = {}
    user = request.user
    if request.method == 'POST':
        pageno = int(request.POST.get('pageno', 1))
        sql = """
        select t.id,t.title,t.user,t.status,t.schedule,ty.name,t.counts from theme t
        inner join type ty on ty.id=t.type
        left join theme_tag tt on tt.theme_id = t.id
        left join tags tg on tg.id=tt.tag_id
        where t.user=%s
        """ % user.id
        type = int(request.POST.get('code', 0))
        tag = int(request.POST.get('tag', 0))
        status = int(request.POST.get('status', 4))
        title = request.POST.get('title', '')
        if type:
            sql += """ and t.type=%s""" %type
        if status != 4:
            sql += """ and t.status=%s""" %status
        if title:
            sql += """ and t.title like'%%%%%s%%%%'""" %title
        if tag:
            sql += """ and tg.id=%s""" %tag

        sql += """ group by t.id order by t.id desc"""

        counts = Theme.objects.filter(user=user.id).count()
        result = get_page(sql, ['id', 'title','user', 'status', 'schedule', 'name', 'counts'], counts, pageno, 30, request.path)
        context['themes'] = result['object_lis']           # 页面内容
        context['page_attr'] = result['page_attr']  # 页面属性
        context['object_id'] = json.dumps(request.POST)
        return render(request, 'manager/manage/themeList.html', context)



def themeView(request, id=None):
    """主题详细页面."""
    context = {}
    user = request.user
    if id:
        theme = Theme.objects.get(pk=id)
        context['themes'] = theme
        return render(request, 'manager/manage/themeview.html', context)


def deltheme(request):
    """删除主题"""
    if request.method == 'POST':
        id = request.POST.get('id')
        ThemeTag.objects.filter(theme__id=id).delete()
        Node.objects.filter(obj__id=id).delete()
        Love.objects.filter(theme__id=id).delete()
        Comment.objects.filter(type=1, obj=id).delete()
        Signal.objects.filter(type=4, obj=id).delete()
        ThemeUrl.objects.filter(theme__id=id).delete()
        Theme.objects.filter(id=id).delete()
        return ajax.ajax_ok()


def changeSchedule(request):
    """更改主题进度"""
    if request.method == 'POST':
        id = request.POST.get('id')
        schedule = request.POST.get('schedule', 0)
        theme = get_object_or_404(Theme, pk=int(id))
        theme.schedule = schedule
        if schedule == '100' and theme.status != 2:
            theme.status = 2
        if theme.status == 0:
            theme.status = 1
        theme.save()
        return ajax.ajax_ok('进度设置成功')