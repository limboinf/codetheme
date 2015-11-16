from django.shortcuts import render
from share.models import Share
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    context = {}
    user = request.user
    title = request.GET.get('title', '')
    share = Share.objects.all().order_by('-id')
    if title:
        share = share.filter(title__contains=title)
    context['share'] = share
    return render(request, 'share/index.html', context)


