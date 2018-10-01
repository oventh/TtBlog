# coding:utf-8

from django.urls import path

from . import views

urlpatterns = [

    # 管理后台页面路由
    path('manage/', views.manage, name="manage"),
    path('manage/content', views.content, name="content"),
    path('manage/addpost', views.addPost, name="addPost"),
    path('manage/editpost/<int:id>', views.editPost, name='editPost'),
    path('manage/category', views.category, name='category'),
    path('manage/comment', views.comment, name='comment'),


]
