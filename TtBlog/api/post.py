from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
import os
import datetime
import json
import re

import blog.models as models


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
    id = request.POST.get('id')
    title = request.POST.get('title')
    content = request.POST.get('content')
    summary = request.POST.get('summary')
    categories = request.POST.get('category')
    tags = request.POST.get('tag')

    # 自动从文章正文中查找图片，将第一张图片作为文章的Banner图
    reg = re.search(r'<img\s+src="(?P<url>.*?)"', content)

    try:

        if id is None or id == '':
            post = models.Post()
            post.Title = title
            post.Content = content
            post.CreateTime = datetime.datetime.now()
            post.CanComment = True
            post.Banner = "" if (reg is None) else reg.group(1)
            post.Summary = summary
            post.User = request.user
            post.save()

            post.Categories.set(json.loads(categories))
            post.Tags.set(json.loads(tags))

        else:
            post = models.Post.objects.get(Id=id)
            post.Title = title
            post.Content = content
            post.CanComment = True
            post.Banner = "" if (reg is None) else reg.group(1)
            post.Summary = summary
            post.save()

            post.Categories.set(json.loads(categories))
            post.Tags.set(json.loads(tags))

        return HttpResponse(json.dumps({'result': True}))
    except Exception as err:
        return HttpResponse(json.dumps({'result': False, 'err': '保存数据时发生异常！Err:{0}'.format(err)}))


def getCategories(request):

    categories = models.Category.objects.all().values()
    data = []
    for c in categories:
        data.append({
            'Id': c['Id'],
            'Name': c['Name'],
            'Checked': False,
        })

    return HttpResponse(json.dumps(data))


def getTags(request):

    tags = models.Tag.objects.all().values()
    data = []
    for t in tags:
        data.append({
            'Id': t['Id'],
            'Name': t['Name'],
            'Checked': False
        })

    return HttpResponse(json.dumps(data))


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
    posts = models.Post.objects.order_by('-Id')[beginNum:endNum].values()

    # 理想状态是一条语句把关联的User对象也查询出来，不过查了半天，只有下面这种解决办法。。。回头再找找！！
    for p in posts:
        user = User.objects.get(id=p['User_id'])
        if user is not None:
            p['username'] = user.username
            p['first_name'] = user.first_name
            p['last_name'] = user.last_name

    totalPage = 0
    if count % pageSize == 0:
        totalPage = count // pageSize
    else:
        totalPage = count // pageSize + 1

    return JsonResponse({'result': list(posts), 'total': count, 'totalPage': totalPage})


def getPost(request):
    id = request.GET.get('id')
    if id is None:
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    post = models.Post.objects.get(Id=id)
    cids, tids = [], []
    for c in post.Categories.all().values('Id'):
        cids.append(c['Id'])

    for t in post.Tags.all().values('Id'):
        tids.append(t['Id'])

    temp = {'Id': post.Id, 'Title': post.Title, 'Content': post.Content, 'Summary': post.Summary,
            'CanComment': post.CanComment, 'cids': cids, 'tids': tids}

    return JsonResponse({'result': True, 'data': temp})


def saveCategory(request):
    id = request.GET.get('id')
    name = request.GET.get('name')

    if name is None or name == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    if id is None or id == '':

        info = models.Category()
        info.Name = name
        info.save()
    else:
        info = models.Category.objects.get(Id=id)
        info.Name = name
        info.save()

    return JsonResponse({'result': True})


def removeCategory(request):
    id = request.GET.get('id')

    if id is None or id == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    info = models.Category.objects.get(Id=id)

    if info is None:
        return JsonResponse({'result': False, 'err': '未找到操作相关的对象！'})

    info.delete()

    return JsonResponse({'result': True})


def saveTag(request):
    id = request.GET.get('id')
    name = request.GET.get('name')

    if name is None or name == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    if id is None or id == '':

        tag = models.Tag()
        tag.Name = name
        tag.save()
    else:
        tag = models.Tag.objects.get(Id=id)
        tag.Name = name
        tag.save()

    return JsonResponse({'result': True})


def removeTag(request):
    id = request.GET.get('id')

    if id is None or id == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    tag = models.Tag.objects.get(Id=id)

    if tag is None:
        return JsonResponse({'result': False, 'err': '未找到操作相关的对象！'})

    tag.delete()

    return JsonResponse({'result': True})

