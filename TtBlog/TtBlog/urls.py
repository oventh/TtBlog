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
from django.views.static import serve
from django.conf.urls import url

from . import settings

urlpatterns = [

    # 前台展示页面路由
    path("", include("blog.urls")),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 后台管理页面路由
    path("manage/", include("manage.urls")),

    # 数据处理接口路由
    path('api/', include('api.urls')),
    path('api/savepost/', include('api.urls')),
    path('api/savecomment', include('api.urls')),

    # 用于微信公众号业务域名的验证文件的访问
    # url(r'^(?P<path>v0gmiYE0PG.txt)$', serve, {'document_root': settings.BASE_DIR}),

    # django 预留
    path('admin/', admin.site.urls),


    






    
]
