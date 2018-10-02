from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import django.contrib.auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect

from . import models


def index(request):
    category = request.GET.get('category')
    tag = request.GET.get('tag')
    page = request.GET.get('page')

    beginNum, endNum = 0, 15

    if page is None or not page.isdigit():
        page = 0
        beginNum, endNum = 0, 15
    else:
        page = int(page)
        beginNum = (page - 1) * 15
        endNum = beginNum + 15

    posts = []
    count = 0

    if category != None and category.isdigit():
        count = models.Post.objects.filter(Categories__in=[category]).count()
        posts = models.Post.objects.filter(Categories__in=[category]).order_by('-Id')[beginNum:endNum]
    elif tag != None and tag.isdigit():
        count = models.Post.objects.filter(Tags__in=[tag]).count()
        posts = models.Post.objects.filter(Tags__in=[tag]).order_by('-Id')[beginNum:endNum]
    else:
        count = models.Post.objects.all().count()
        posts = models.Post.objects.order_by('-Id')[beginNum:endNum]

    categories = models.Category.objects.all()
    tags = models.Tag.objects.all()
    site = models.Site.objects.get()

    totalPage = 0
    if count % 15 == 0:
        totalPage = count // 15
    else:
        totalPage = count // 15 + 1

    return render(request, "blog/index.html", {'site': site, 'posts': posts, 'categories': categories, 'tags': tags,
                                               'category': category, 'tag': tag, 'page': page, 'totalPage': totalPage,
                                               'totalRecord': count})


def post(request, id):
    site = models.Site.objects.get()

    if id is None:
        return render(request, "blog/post.html", {'site': site})

    post = models.Post.objects.get(Id=id)

    count = models.Comment.objects.filter(Post=id).count()
    comments = models.Comment.objects.filter(Post=id).order_by('-Id')
    commentsList = []
    for c in comments:
        if c.RecommentId is None:
            temp = {'Id': c.Id, 'Creator': c.Creator, 'CreateTime': c.CreateTime, 'PostId': c.Post_id,
                    'RecommentId': c.RecommentId, 'Content': c.Content}
            childs = []
            for t in comments:
                if t.RecommentId == c.Id:
                    childs.append({'Id': t.Id, 'Creator': t.Creator, 'CreateTime': t.CreateTime, 'PostId': t.Post_id,
                                   'RecommentId': t.RecommentId, 'Content': t.Content})

            temp['childs'] = childs
            commentsList.append(temp)

    return render(request, "blog/post.html", {'site': site, 'post': post, 'comments': commentsList, 'count': count})


def login(request):
    return render(request, "manage/login.html")


@csrf_protect
def doLogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    nextUrl = request.POST.get("next")

    if username == None or username == '' or password == None or password == '':
        return render(request, "manage/login.html", {"err": "用户名和密码不能为空！"})

    user = django.contrib.auth.authenticate(username=username, password=password)
    if user is None:
        return render(request, "manage/login.html", {"err": "用户名或密码不正确！"})
    else:
        django.contrib.auth.login(request, user)
        if nextUrl is not None:
            return redirect(nextUrl)
        else:
            return redirect("/manage")


def logout(request):
    logout(request)
    return redirect("/")
