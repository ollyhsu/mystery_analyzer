import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from vulscan.models import SolUpload


# Create your views here.


@login_required
def vulscan(request):
    return render(request, "vulscan.html")


def sol_upload_handle(request):
    # sol = request.FILES.get('upload_file').read()
    # sol = request.FILES['upload_file']
    '''sol上传处理页'''
    # 【1】得到sol
    sol = request.FILES['upload_file']
    # 【2】拼接sol保存路径+sol名
    if not os.path.isdir("%s/file_upload" % settings.MEDIA_ROOT):
        os.makedirs("%s/file_upload" % settings.MEDIA_ROOT)
    save_path = "%s/file_upload/%s" % (settings.MEDIA_ROOT, sol.name)

    # 【3】保存sol到指定路径，因为图片是2进制式，因此用wb，
    with open(save_path, 'wb') as f:
        for content in sol.chunks():
            f.write(content)

    # 【4】保存图片路径到数据库，此处只保存其相对上传目录的路径
    SolUpload.objects.create(fpath='file_upload/%s' % sol.name)

    # 【5】别忘记返回信息
    # return HttpResponse('上传成功，图片地址：file_upload/%s' % sol.name)
    return JsonResponse({"res": 1})
