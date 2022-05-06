from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings


# Create your views here.


@login_required
def vulscan(request):
    return render(request, "vulscan.html")


def upload_handle(request):
    # '''sol上传处理页'''
    # # 【1】得到图片
    # sol = request.FILES['sol']
    # # 【2】拼接图片保存路径+图片名
    # save_path = "%s/file_upload/%s" % (settings.MEDIA_ROOT, sol.name)
    # # 【3】保存图片到指定路径，因为图片是2进制式，因此用wb，
    # with open(save_path, 'wb') as f:
    #     # pic.chunks()为图片的一系列数据，它是一一段段的，所以要用for逐个读取
    #     for content in pic.chunks():
    #         f.write(content)

    # 【4】保存图片路径到数据库，此处只保存其相对上传目录的路径
    # PicTest.objects.create(goods_pic='app1/%s' % pic.name)

    # 【5】别忘记返回信息
    return HttpResponse(settings.MEDIA_ROOT)
