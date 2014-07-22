#coding=utf-8
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """通过邮箱，密码创建用户"""
    def create_user(self, email,username, password=None,type=None,**kwargs):
        if not email:
            raise ValueError(u'用户必须要有邮箱')

        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
            type=type if type else 0
        )
        user.set_password(password)
        if kwargs:
            if kwargs.get('sex', None): user.sex = kwargs['sex']
            if kwargs.get('is_active', None): user.is_active=kwargs['is_active']
            if kwargs.get('uid', None): user.uid=kwargs['uid']
            if kwargs.get('access_token', None): user.access_token=kwargs['access_token']
            if kwargs.get('url', None): user.url=kwargs['url']
            if kwargs.get('desc', None): user.desc=kwargs['desc']
            if kwargs.get('avatar', None): user.avatar=kwargs['avatar']

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """扩展User"""
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True,db_index=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type = models.IntegerField(default=0)                   # 类型，0本站，1微博登录
    sex = models.IntegerField(default=1)                    # sex
    uid = models.CharField(max_length=50, null=True)                    # weibo uid
    access_token = models.CharField(max_length=100, null=True)          # weibo access_token
    url = models.URLField(null=True)                            # 个人站点
    desc = models.CharField(max_length=2000, null=True)         # 个人信息简介
    avatar = models.CharField(max_length=500, null=True)        # 头像
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    class Meta:
        db_table = 'user'


class CustomAuth(object):
    """自定义用户验证"""
    def authenticate(self, email=None, password=None):
        try:
            user = MyUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except MyUser.DoesNotExist:
            return None