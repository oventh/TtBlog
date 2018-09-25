# coding:utf-8

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:id>', views.post, name="post"),
    path('login', views.login, name="login"),
    path('dologin', views.doLogin, name="dologin"),
    path('logout', views.logout, name="logout"),

    path('manage/', views.manage, name="manage"),
    path('manage/content', views.content, name="content"),
    path('manage/addpost', views.addPost, name="addPost"),
]