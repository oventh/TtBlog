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
    path("manage/", include("blog.urls")),
    path("manage/content", include("blog.urls")),
    path('manage/addpost', include("blog.urls")),
    path('manage/editpost', include("blog.urls")),


    # 数据处理接口路由
    path('api/upload', include("blog.urls")),
    path('api/savepost', include("blog.urls")),
    path('api/getcategories', include("blog.urls")),
    path('api/gettags', include("blog.urls")),
    path('api/removepost', include("blog.urls")),
    path('api/querypost', include("blog.urls")),


    # django 预留
    path('admin/', admin.site.urls),
    
]
