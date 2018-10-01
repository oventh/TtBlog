# coding:utf-8

from django.urls import path

from . import post

urlpatterns = [

    # post controllers
    path('api/upload', post.upload, name='upload'),
    path('api/getcategories', post.getCategories, name='getCategories'),
    path('api/gettags', post.getTags, name='getTags'),
    path('api/savepost', post.savePost, name='savePost'),
    path('api/removepost', post.removePost, name='removePost'),
    path('api/querypost', post.queryPost, name='queryPost'),
    path('api/getpost', post.getPost, name='getPost'),
    path('api/savecategory', post.saveCategory, name='saveCategory'),
    path('api/removecategory', post.removeCategory, name='removeCategory'),
    path('api/savetag', post.saveTag, name='saveTag'),
    path('api/removetag', post.removeTag, name='removeTag'),


    # comment controllers



]