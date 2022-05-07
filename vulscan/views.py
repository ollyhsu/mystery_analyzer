import os
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings

from mytools.views import eth_add_parser
from vulscan.models import SolAddList


# Create your views here.


@login_required
def vulscan(request):
    return render(request, "vulscan.html")


@login_required
def sol_upload_handle(request):
    stime = time.time()
    # print(int(stime))
    # sol = request.FILES.get('upload_file').read()
    # sol = request.FILES['upload_file']
    '''sol上传处理页'''
    # 【1】得到sol
    sol = request.FILES['upload_file']
    # 【2】拼接sol保存路径+sol名
    if not os.path.isdir("%s/file_upload" % settings.MEDIA_ROOT):
        os.makedirs("%s/file_upload" % settings.MEDIA_ROOT)
    file_name, extension_name = os.path.splitext(sol.name)
    tname = "%s-%s%s" % (file_name, int(stime), extension_name)
    save_path = "%s/file_upload/%s" % (settings.MEDIA_ROOT, tname)

    # 【3】保存sol到指定路径，因为图片是2进制式，因此用wb，
    with open(save_path, 'wb') as f:
        for content in sol.chunks():
            f.write(content)

    # 【4】保存路径到数据库，此处只保存其相对上传目录的路径
    SolAddList.objects.create(fname=sol.name, fpath='file_upload/%s' % tname, scantype="file", time=int(stime),
                              uid=request.user.id)

    # 【5】别忘记返回信息
    return JsonResponse({"res": 1})


@login_required
def ether_add_handle(request):
    stime = time.time()
    ether_add = request.POST.get("ether_add")
    if ether_add[:2] == '0x':
        tname = "%s-%s.sol" % (ether_add, int(stime))
        add_path = "%s/eth_add/%s" % (settings.MEDIA_ROOT, tname)
        eth_add_parser(ether_add, add_path)
        # 【4】保存路径到数据库，此处只保存其相对上传目录的路径
        SolAddList.objects.create(add=ether_add, fpath='eth_add/%s' % tname, scantype="add", time=int(stime),
                                  uid=request.user.id)
        return JsonResponse({"res": 1})
    else:
        return JsonResponse({"res": 0})
