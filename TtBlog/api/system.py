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

    setting = models.Site.objects.all()[0]
    data = {'Id': setting.Id, 'Name': setting.Name, 'Summary': setting.Summary, 'Banner': setting.Banner, 'PageSize': setting.PageSize}

    return JsonResponse({'result': data})


@csrf_protect
def saveSetting(request):

    name = request.POST.get('name')
    summary = request.POST.get('summary')
    banner = request.POST.get('banner')
    pageSize = request.POST.get('pageSize')

    if name is None or name == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    sites = models.Site.objects.all()
    for s in sites:
        s.delete()

    setting = models.Site()
    setting.Name = name
    setting.Summary = summary
    setting.Banner = banner
    setting.PageSize = pageSize

    setting.save()

    return JsonResponse({'result': True})
