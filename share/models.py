#coding=utf-8
from manager.models import MyUser
from django.db import models


class Share(models.Model):
    title = models.CharField(max_length=100)
    user = models.IntegerField()
    url = models.URLField()
    add_date = models.DateTimeField(auto_now=True,auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'share'

    def getUser(self):
        """返回用户对象"""
        return MyUser.objects.get(pk=self.user)



