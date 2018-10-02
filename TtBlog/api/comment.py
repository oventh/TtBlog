from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import os
import datetime
import json
import re

import blog.models as models


def query(request):
    pageSize = int(request.GET.get('pageSize'))
    pageIndex = int(request.GET.get('pageIndex'))

    beginNum = (pageIndex - 1) * pageSize
    endNum = beginNum + pageSize

    count = models.Comment.objects.count()
    comments = models.Comment.objects.order_by('-Id')[beginNum:endNum]

    data = []

    for c in comments:
        data.append({'Id': c.Id, 'Content': c.Content, 'PostId': c.Post_id, 'PageTitle': c.Post.Title,
                  'CreateTime': c.CreateTime, 'Creator': c.Creator})


    totalPage = 0
    if count % pageSize == 0:
        totalPage = count // pageSize
    else:
        totalPage = count // pageSize + 1

    return JsonResponse({'result': data, 'total': count, 'totalPage': totalPage})


@csrf_protect
def saveComment(request):
    postId = request.POST.get('postId')
    creator = request.POST.get('creator')
    content = request.POST.get('content')
    recomment = request.POST.get('recomment')

    if postId is None or postId == '' or creator is None or creator == '' or content is None or content == '':
        return JsonResponse({'result': False, 'err': '调用方法必要缺要的参数！'})

    comment = models.Comment()
    comment.Creator = creator
    comment.Post_id = int(postId)
    comment.Content = content
    comment.CreateTime = datetime.datetime.now()

    if recomment is not None and recomment != '':
        comment.RecommentId = int(recomment)

    comment.save()

    return JsonResponse({'result': True})


def removeComment(request):
    id = request.GET.get('id')
    if id is None or id == '':
        return JsonResponse({'result': False, 'err': '调用方法缺少必要的参数！'})

    info = models.Comment.objects.get(Id=id)
    if info is None:
        return JsonResponse({'result': False, 'err': '未找到操作相关的对象！'})

    info.delete()

    return JsonResponse({'result': True})
