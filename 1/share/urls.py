from django.conf.urls import patterns, include, url
#
urlpatterns = patterns('share.views',
    url(r'^$', 'index', name='share_index'),
)
