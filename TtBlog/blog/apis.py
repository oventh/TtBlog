from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.conf import settings
import os
import datetime
import json
import re

from . import models


@csrf_protect
def upload(request):
    urls = []
    try:
        for k in request.FILES.keys():
            img = request.FILES.get(k)
            rootDir = datetime.datetime.now().strftime('%y%m%d')    # 以日期做为存储图片的最后一级目录
            saveDir = os.getcwd() + '/blog/static/upload/{0}'.format(rootDir)
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)

            savePath = os.path.join(saveDir, img.name)
            with open(savePath, 'wb+') as p:
                for data in img.chunks():
                    p.write(data)

            url = "/static/upload/{0}/{1}".format(rootDir, img.name)
            urls.append(url)

        return HttpResponse(json.dumps({'errno': 0, 'data': urls}), content_type="application/json")
    except IOError as err:
        return HttpResponse(json.dumps({'errno': 1, 'data': [], 'error': err}), content_type="application/json")


@csrf_protect
def savePost(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
    summary = request.POST.get('summary')
    categories = request.POST.get('category')
    tags = request.POST.get('tag')

    reg = re.search(r'<img\s+src="(?P<url>.*?)"', content)

    try:
        post = models.Post()
        post.Title = title
        post.Content = content
        post.CreateTime = datetime.datetime.now()
        post.CanComment = True
        post.Banner = "" if (reg is None) else reg.group(1)
        post.Summary = summary
        post.User = request.user
        post.save()

        if categories is not None:
            for c in json.loads(categories):
                post.Categories.add(c)

        if tags is not None:
            for t in json.loads(tags):
                post.Tags.add(t)

        post.save()

        return HttpResponse(json.dumps({'result': True}))
    except Exception as err:
        return HttpResponse(json.dumps({'result': False, 'err': '保存数据时发生异常！Err:{0}'.format(err)}))


def getCategories(request):

    categories = models.Category.objects.all().values()
    return HttpResponse(json.dumps(list(categories)))


def getTags(request):

    tags = models.Tag.objects.all().values()
    return HttpResponse(json.dumps(list(tags)))


def removePost(request):
    id = request.GET.get('id')
    if id is None:
        return HttpResponse(json.dumps({'result': False, 'err': '调用方法缺少必要的参数！'}))

    post = models.Post.objects.get(Id=id)
    if post is None:
        return HttpResponse(json.dumps({'result': False, 'err': '未找到相关的文章！'}))

    post.delete()
    return HttpResponse(json.dumps({'result': True}))


def queryPost(request):
    pageSize = int(request.GET.get('pageSize'))
    pageIndex = int(request.GET.get('pageIndex'))

    beginNum = (pageIndex - 1) * pageSize
    endNum = beginNum + pageSize

    count = models.Post.objects.count()
    posts = models.Post.objects.order_by('-Id')[beginNum:endNum].values('Id', 'User__user')

    totalPage = 0
    if count % pageSize == 0:
        totalPage = count // pageSize
    else:
        totalPage = count // pageSize + 1

    # json = serializers.serialize('json', posts)

    return JsonResponse({'result': list(posts), 'total': count, 'totalPage': totalPage})
