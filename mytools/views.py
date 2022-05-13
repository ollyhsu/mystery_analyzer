import json
import os
import sys

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pyevmasm import disassemble_hex, assemble_hex

from mystery_analyzer.settings import MEDIA_ROOT
from vulscan.views import get_bin_file, run_file_check
from .models import EtherVerified, EtherDeatilList
from .platform.ethget import sync_main_code_sql, eth_add_parser, update_url_sql


# Create your views here.


def disassembler(request):
    return render(request, "disassembler.html")


def disassembler_ajax_handle(request):
    # ajax 汇编处理
    bincode = request.POST.get("bincode")
    if bincode[:10] == '0x60806040' or bincode[:8] == '60806040':
        opcode_from_bytecode = disassemble_hex(bincode)
        return JsonResponse({"res": 1, "opcode": opcode_from_bytecode})
    elif bincode[:4] == 'PUSH':
        opcode_inline = "\n".join(bincode.splitlines())
        bytecode_from_opcode = assemble_hex(opcode_inline)
        return JsonResponse({"res": 2, "runtime": bytecode_from_opcode})
    else:
        # 用户名和密码错误
        return JsonResponse({"res": 0})


def etherscansync(request):
    count = 0
    s_list = []
    ether_datas = EtherVerified.objects.all()[::-1]
    for etherlistware in ether_datas:
        ether_data = {
            'id': etherlistware.id,
            'add': etherlistware.add,
            'name': etherlistware.name,
            'compiler': etherlistware.compiler,
            'version': etherlistware.version,
            'verified_time': etherlistware.verified_time,
            'url': etherlistware.url,
            'fpath': etherlistware.fpath,

        }
        s_list.append(ether_data)
        count += 1
    data = s_list
    return render(request, "etherscan.html", {"data": data})


def save_sol_ajax(request):
    # ajax sync处理
    sync_main_code_sql()
    return JsonResponse({"res": 1})


def update_list_ajax(request):
    # ajax sync处理
    sys.setrecursionlimit(1500)
    update_url_sql()
    print("update success")
    return JsonResponse({"res": 1})


# 按钮保存代码
def save_sync_each_file(request):
    rid_get = request.POST.get('rid')
    # print(rid_get)
    try:
        obj = EtherVerified.objects.get(id=rid_get)
        filename = obj.add + "-" + obj.name + ".sol"
        save_path = "%s/etherscan/%s" % (MEDIA_ROOT, filename)
        sql_fpath = 'etherscan/%s' % filename
        if obj.fpath is None:
            eth_add_parser(obj.add, save_path)
            obj.fpath = sql_fpath
            obj.save()
        return JsonResponse({"res": 1})
    except Exception as e:
        print(e)
        return HttpResponse('当前报告不存在')


# 按钮删除etherscan报告
def del_sync_each_file(request):
    rid_get = request.POST.get('rid')
    try:
        dreport_datas = EtherDeatilList.objects.filter(rid=rid_get)
        if len(dreport_datas) > 0:
            for deatillistware in dreport_datas:
                deatillistware.delete()
        else:
            print('没有数据')
        obj = EtherVerified.objects.get(id=rid_get)
        # 循环获取obj.cfg文件路径
        if obj.cfg:
            for i in json.loads(obj.cfg):
                cfg_path = os.path.join(settings.MEDIA_ROOT, i)
                # delete file
                if os.path.exists(cfg_path):
                    os.remove(cfg_path)
        if obj.fpath:
            file_path = os.path.join(settings.MEDIA_ROOT, obj.fpath)
            if os.path.exists(file_path):
                os.remove(file_path)
        obj.delete()
        print("Delete Done")
        return JsonResponse({"res": 1})
    except Exception as e:
        print(e)
        return JsonResponse({"res": 0})


# 按钮提交检查
def check_sync_each_file(request):
    rid_get = request.POST.get('rid')
    obj = EtherVerified.objects.get(id=rid_get)
    abs_path = "%s/%s" % (MEDIA_ROOT, obj.fpath)
    version = obj.version
    # print(abs_path)
    # 获取Runtime
    obj.runtime = get_bin_file(abs_path, eth_ver=version)
    # 返回CFG PNG List
    # obj.cfg = get_cfg_png_list(abs_path)
    # 运行检测
    result, check_time = run_file_check(abs_path)
    obj.result, obj.check_time = result, check_time
    obj.status = "completed"
    obj.save()
    print("Save Done...")
    return JsonResponse({"res": 1})
