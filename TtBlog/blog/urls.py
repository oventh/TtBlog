# coding:utf-8

from django.urls import path

from . import views

urlpatterns = [

    # 前台展示页面路由
    path('', views.index, name="index"),
    path('post/<int:id>', views.post, name="post"),
    path('login', views.login, name="login"),
    path('dologin', views.doLogin, name="dologin"),
    path('logout', views.logout, name="logout"),


]