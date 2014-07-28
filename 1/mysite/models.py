#coding=utf-8
from django.conf import settings
from django.db import models
from wmd import models as wmd_models        # 导入wmd的models
from manager.models import MyUser
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import markdown


class Type(models.Model):
    """分类"""
    name = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'type'

        

class Theme(models.Model):
    """编程主题"""
    title = models.CharField(max_length=100)
    user = models.IntegerField()
    type = models.IntegerField(default=0)
    content = wmd_models.MarkDownField()
    content_show = wmd_models.MarkDownField(u'正文显示', null=True)
    add_date = models.DateTimeField()
    is_great = models.IntegerField(default=0)   # 是否精华
    counts = models.IntegerField(default=0)     # 点击率
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Theme, self).save()

    class Meta:
        db_table = 'theme'

    def getUser(self):
        """返回用户对象"""
        return MyUser.objects.get(pk=self.user)

    def getLove(self):
        """返回关注数"""
        return Love.objects.filter(theme=self.id).count()

    def getLoveObj(self):
        """返回关注数"""
        return Love.objects.filter(theme=self.id).values_list('user', flat=True)

    def getTags(self):
        """获取标签"""
        return ThemeTag.objects.filter(theme=self.id)

    def getType(self):
        """获取类型"""
        return Type.objects.get(pk=self.type)



class Tag(models.Model):
    """个人标签"""
    name = models.CharField(max_length=100)
    user = models.IntegerField()
    add_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'tags'



class ThemeTag(models.Model):
    """主题标签"""
    theme = models.ForeignKey(Theme)
    tag = models.ForeignKey(Tag)
    add_time = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return set.tag.name
    class Meta:
        db_table = 'theme_tag'





class Love(models.Model):
    """关注"""
    theme = models.ForeignKey(Theme)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    add_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'love'


class Comment(models.Model):
    """评论"""
    type = models.IntegerField(default=1)           # 1:theme;2:share
    obj = models.IntegerField()                     # 评论对象id
    user = models.ForeignKey(settings.AUTH_USER_MODEL)      # 用户
    content = wmd_models.MarkDownField()
    content_show = wmd_models.MarkDownField(u'正文显示', null=True)
    reply_id = models.IntegerField(default=0)       # 回复的评论id
    reply_user = models.IntegerField(default=0)      # 回复谁
    add_date = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None):
        self.content_show = mark_safe(markdown.markdown(force_unicode(self.content), ['codehilite'], safe_mode='escape'))
        super(Comment, self).save()

    class Meta:
        db_table = 'comment'

class Signal(models.Model):
    """公告"""
    type = models.IntegerField(default=0)        # 0,系统公告；1:评论;2:私信;3.关注;4.主题关注
    obj = models.IntegerField(default=0)         # 对象id
    user = models.ForeignKey(settings.AUTH_USER_MODEL)      # 发布者
    who = models.IntegerField(default=0)                    # 接受者
    title = models.CharField(max_length=200, null=True)        # 标题
    content = models.CharField(max_length=1000, null=True)        # 内容
    status = models.IntegerField(default=0)             # 状态，0，未读；1已读，2.删除
    add_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_signal'

    def getObj(self):
        """获取实例对象"""
        if self.type in (1, 4):
            return Theme.objects.get(pk=self.obj)
        return None



class ThemeUrl(models.Model):
    """theme链接"""
    theme = models.ForeignKey(Theme)
    url = models.URLField()
    is_author = models.IntegerField(default=0)  # 是否是作者
    user = models.ForeignKey(MyUser)
    desc = models.CharField(max_length=500, null=True) # 描述
    add_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'theme_url'

class LoveUser(models.Model):
    """关注的人"""
    user = models.ForeignKey(MyUser)
    who = models.IntegerField()         # 关注者
    add_date = models.DateField(auto_now=True)

    class Meta:
        db_table = 'love_user'

    def getUobj(self):
        """获取用户实例"""
        return MyUser.objects.get(pk=self.who)