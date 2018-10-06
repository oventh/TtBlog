# coding:utf-8

from django.urls import path

from . import views

urlpatterns = [

    # 管理后台页面路由
    path('', views.manage, name="manage"),
    path('content', views.content, name="content"),
    path('addpost', views.addPost, name="addPost"),
    path('editpost/<int:id>', views.editPost, name='editPost'),
    path('comment', views.comment, name='comment'),
    path('setting', views.setting, name='setting'),


]
