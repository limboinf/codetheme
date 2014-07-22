#coding=utf-8
"""
==================================
function:   基于七牛云存储，进行上传处理
addDate:    2014-06-08
author:     BeginMan
==================================
"""
import qiniu.conf
import qiniu.rs
import qiniu.io
import datetime
from PIL import Image
import StringIO
from django.conf import settings

# 初始化七牛环境
qiniu.conf.ACCESS_KEY = settings.QINIU_ACCESS_KEY
qiniu.conf.SECRET_KEY = settings.QINIU_SECRET_KEY

#上传凭证
policy = qiniu.rs.PutPolicy(settings.QINIU_BUCKET_NAME)
uptoken = policy.token()


class SuperQiniu(object):
    def __init__(self, filepath, request=None, **kwargs):
        self.filepath = filepath    # 文件绝对路径
        self.key = datetime.datetime.now()               # 文件唯一标示
        self.request = request
        self.kwargs = kwargs

    def uploadFile(self):
        """上传图片"""
        extra = qiniu.io.PutExtra()
        mime_type = self.filepath.content_type
        extra.mime_type = mime_type
        type = 'PNG'
        if mime_type == 'image/jpeg':
            type = 'JPEG'
        self.filepath.seek(0)
        resize_pic = self.setPic(type)
        ret, err = qiniu.io.put(uptoken, str(self.key), resize_pic, extra)
        if err is not None:
            print 'error:', err
            return
        print settings.QINIU_DOMAIN+'/'+ret['key']
        return settings.QINIU_DOMAIN+'/'+ret['key']

    def downloadFile(self):
        """下载图片"""
        base_url = qiniu.rs.make_base_url(settings.QINIU_DOMAIN, str(self.key))
        policy = qiniu.rs.GetPolicy()
        private_url = policy.make_request(base_url)
        return private_url


    def setPic(self, type):
        """设置160*160大小图片"""
        image = Image.open(self.filepath)
        image.thumbnail((160, 160), Image.ANTIALIAS)
        image_file = StringIO.StringIO()
        image.save(image_file, type, quality=90)
        image_file.seek(0)
        return image_file







