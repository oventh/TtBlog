# coding:utf-8

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:id>', views.post, name="post"),
    path('manage/', views.manage, name="manage"),
    path('manage/content', views.content, name="content"),
]