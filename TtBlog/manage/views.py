from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

import blog.models as models


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
def setting(request):
    return render(request, "manage/setting.html")


@login_required(login_url='/login')
def editPost(request, id):
    if id is None:
        return HttpResponse(json.dumps({'result': False, 'error': '调用方法缺少必要的参数！'}))

    return render(request, 'manage/addpost.html', {'id': id})


@login_required(login_url="/login")
def comment(request):

    return render(request, "manage/comment.html")