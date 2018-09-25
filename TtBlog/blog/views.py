from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
import hashlib

from . import models
# Create your views here.

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
    remember = request.POST.get("remember")

    if username == None or username == '' or password == None or password == '':
        return render(request, "manage/login.html",{"err": "用户名和密码不能为空！"})

    user = models.User.objects.filter(Username = username).first()
    if user == None or user.Password != hashlib.md5(password.encode(encoding='UTF-8')).hexdigest():
        return render(request, "manage/login.html",{"err": "用户名或密码不正确！"})

    request.session["__loginUserId__"] = user.Id
    request.session["__loginNickname__"] = user.Nickname
    

    return redirect("/manage")


def logout(request):
    del request.session["__loginUserId__"]
    return redirect("/")


def checkAuth(request):
    if request.session["__loginUserId__"] == None:
        return redirect("/login")


# manage site controller #

def manage(request):
    checkAuth(request)    

    return render(request, "manage/index.html")


def content(request):
    checkAuth(request)

    page = request.GET.get("page")

    beginNum, endNum = 0, 15

    if page == None or not page.isdigit():
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


def addPost(request):
    checkAuth(request)

    return render(request, "manage/addpost.html")


def category(request):
    checkAuth(request)

    return render(request, "manage/category.html")


def comment(request):
    checkAuth(request)

    return render(request, "manage/comment.html")


def setting(request):
    checkAuth(request)

    return render(request, "manage/setting.html")

   