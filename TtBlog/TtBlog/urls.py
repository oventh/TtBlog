"""TtBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    # 前台展示页面路由
    path("", include("blog.urls")),
    path("post/<int:id>", include("blog.urls")),
    path('login', include("blog.urls")),
    path('dologin', include("blog.urls")),
    path('logout', include("blog.urls")),


    # 后台管理页面路由
    path("manage/", include("manage.urls")),
    path("manage/content", include("manage.urls")),
    path('manage/addpost', include("manage.urls")),
    path('manage/editpost', include("manage.urls")),
    path('manage/category', include("manage.urls")),
    path('manage/comment', include("manage.urls")),


    # 数据处理接口路由
    path('api/upload', include("api.urls")),
    path('api/savepost', include("api.urls")),
    path('api/getcategories', include("api.urls")),
    path('api/gettags', include("api.urls")),
    path('api/removepost', include("api.urls")),
    path('api/querypost', include("api.urls")),
    path('api/getpost', include("api.urls")),
    path('api/savecategory', include('api.urls')),
    path('api/removecategory', include('api.urls')),
    path('api/savetag', include('api.urls')),
    path('api/removetag', include('api.urls')),


    # django 预留
    path('admin/', admin.site.urls),
    
]
