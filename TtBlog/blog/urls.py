# coding:utf-8

from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('post/<int:id>', views.post, name="post"),
]