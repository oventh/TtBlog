# coding:utf-8

from django.urls import path

from . import post, comment, system

urlpatterns = [

    # post controllers
    path('upload', post.upload, name='upload'),
    path('getcategories', post.getCategories, name='getCategories'),
    path('gettags', post.getTags, name='getTags'),
    path('savepost', post.savePost, name='savePost'),
    path('removepost', post.removePost, name='removePost'),
    path('querypost', post.queryPost),
    path('getpost', post.getPost, name='getPost'),
    path('savecategory', post.saveCategory, name='saveCategory'),
    path('removecategory', post.removeCategory, name='removeCategory'),
    path('savetag', post.saveTag, name='saveTag'),
    path('removetag', post.removeTag, name='removeTag'),


    # comment controllers
    path('querycomment', comment.query, name='queryComment'),
    path('savecomment', comment.saveComment, name='saveComment'),
    path('removecomment', comment.removeComment, name='removeComment'),


    # system controllers
    path('getSetting', system.getSetting, name='getSetting'),
    path('saveSetting', system.saveSetting, name='saveSetting'),



]