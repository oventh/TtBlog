from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import django.contrib.auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
from django.http import HttpResponse
import os
import datetime
import json
import re

from . import models


def index(request):

    category = request.GET.get('category')
    tag = request.GET.get('tag')
    page = request.GET.get('page')

    beginNum, endNum = 0, 15

    if page == None or not page.isdigit():
        page = 0
        beginNum, endNum = 0, 15
    else:
        page = int(page)
        beginNum = (page + 1) * 15
        endNum = beginNum + 15

    posts = []

    if category != None and category.isdigit():
        posts = models.Post.objects.filter(Categories__in = [category]).order_by('-Id')[beginNum:endNum]
    elif tag != None and tag.isdigit():
        posts = models.Post.objects.filter(Tags__in = [tag]).order_by('-Id')[beginNum:endNum]
    else:
        posts = models.Post.objects.order_by('-Id')[beginNum:endNum]
    
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    site = models.Site.objects.get()

    return render(request, "blog/index.html", {'site': site, 'posts': posts, 'categories': categories, 'tags': tags})


def post(request, id):

    site = models.Site.objects.get()

    if id is None:
        return render(request, "blog/post.html", {'site': site})

    post = models.Post.objects.get(Id=id)
    comments = models.Comment.objects.filter(Post = id).order_by('-Id')

    return render(request, "blog/post.html", {'site': site, 'post': post, 'comments': comments})


def login(request):
    return render(request, "manage/login.html")


@csrf_protect
def doLogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    nextUrl = request.POST.get("next")

    if username == None or username == '' or password == None or password == '':
        return render(request, "manage/login.html",{"err": "用户名和密码不能为空！"})

    user = django.contrib.auth.authenticate(username= username, password = password)
    if user is None:
        return render(request, "manage/login.html",{"err": "用户名或密码不正确！"})
    else:
        django.contrib.auth.login(request, user)
        if nextUrl is not None:
            return redirect(nextUrl)
        else:
            return redirect("/manage")


def logout(request):
    logout(request)
    return redirect("/")


# manage site controller #


@login_required(login_url="/login")
def manage(request):

    return render(request, "manage/index.html")


@login_required(login_url="/login")
def content(request):

    page = request.GET.get("page")

    beginNum, endNum = 0, 15

    if page is None or not page.isdigit():
        page = 0
        beginNum, endNum = 0, 15
    else:
        page = int(page)
        beginNum = page * 15
        endNum = beginNum + 15
    
    count = models.Post.objects.count()
    posts = models.Post.objects.order_by('-Id')[beginNum:endNum]

    totalPage = 0
    if count % 15 == 0: 
        totalPage = count // 15 
    else: 
        totalPage = count // 15 + 1

    return render(request, "manage/content.html", {'posts': posts, 'page': page, 'totalPage': totalPage})


@login_required(login_url="/login")
def addPost(request):
    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()

    return render(request, "manage/addpost.html", {'categories': categories, 'tags': tags})


@login_required(login_url="/login")
def category(request):

    return render(request, "manage/category.html")


@login_required(login_url="/login")
def comment(request):

    return render(request, "manage/comment.html")


@login_required(login_url="/login")
def setting(request):
    return render(request, "manage/setting.html")


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




