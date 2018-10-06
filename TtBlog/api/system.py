from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, JsonResponse
import os
import datetime
import json
import re

from blog import models
from TtBlog import settings


def getSetting(request):

    setting = models.Setting.objects.all()[0]

    return JsonResponse({'result': setting})


def saveSetting(request):

    name = request.POST.get('name')
    summary = request.POST.get('summary')
    banner = request.POST.get('banner')
    pageSize = request.POST.get('pageSize')

    if name is None or name == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    setting = models.Setting()
    setting.Name = name
    setting.Summary = summary
    setting.PageSize = pageSize

    setting.save()

    return JsonResponse({'result': True})
