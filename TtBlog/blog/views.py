from django.shortcuts import render
from django.http import HttpResponse
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


