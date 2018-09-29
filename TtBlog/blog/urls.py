# coding:utf-8

from django.urls import path
from . import views, apis


urlpatterns = [

    # 前台展示页面路由
    path('', views.index, name="index"),
    path('post/<int:id>', views.post, name="post"),
    path('login', views.login, name="login"),
    path('dologin', views.doLogin, name="dologin"),
    path('logout', views.logout, name="logout"),


    # 管理后台页面路由
    path('manage/', views.manage, name="manage"),
    path('manage/content', views.content, name="content"),
    path('manage/addpost', views.addPost, name="addPost"),
    path('manage/editpost/<int:id>', views.editPost, name='editPost'),


    # 数据处理接口路由
    path('api/upload', apis.upload, name='upload'),
    path('api/getcategories', apis.getCategories, name='getCategories'),
    path('api/gettags', apis.getTags, name='getTags'),
    path('api/savepost', apis.savePost, name='savePost'),
    path('api/removepost', apis.removePost, name='removePost'),
    path('api/querypost', apis.queryPost, name='queryPost'),
    path('api/getpost', apis.getPost, name='getPost'),



]