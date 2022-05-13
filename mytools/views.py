import json
import os
import sys
import time

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pyevmasm import disassemble_hex, assemble_hex

from mystery_analyzer.settings import MEDIA_ROOT
from vulreport.views import get_sol_code_file
from vulscan.views import get_bin_file, run_file_check, get_cfg_png_list
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
            'status': etherlistware.status
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
        if obj.result:
            report_file = os.path.join(MEDIA_ROOT, obj.result)
            if os.path.exists(report_file):
                os.remove(report_file)
        obj.delete()
        print("Delete Done")
        return JsonResponse({"res": 1})
    except Exception as e:
        print(e)
        return JsonResponse({"res": 0})


def get_report_json_eth(data, rid):
    try:
        # # 转成字典格式
        dict_datas = json.loads(data)
        myth_data = dict_datas[0].get('Mythril')
        sli_data = dict_datas[1].get('Slither')

        if myth_data is not None:
            if myth_data['success'] and myth_data['error'] is None:
                # myth_info = "Mythril has detected the vulnerability.\n"
                for issue in myth_data['issues']:
                    try:
                        EtherDeatilList.objects.create(rid=rid, swcid=issue['swc-id'], title=issue['title'],
                                                     impact=issue['severity'], lines=issue['lineno'],
                                                     description=issue['description'])
                    except Exception as e:
                        print(e)
            elif myth_data['success'] is False:
                # myth_status = "failed"
                print(myth_data['error'])
            else:
                myth_info = "Mythril has detected the vulnerability.\n"
        else:
            myth_info = "Mythril does not detect vulnerabilities.\n"

        if sli_data is not None:
            if sli_data['success'] and sli_data['error'] is None:
                # sli_info = "Slither has detected the vulnerability.\n"
                for detector in sli_data['results']['detectors']:
                    if detector['impact'] not in ['Informational', 'Optimization']:
                        try:
                            EtherDeatilList.objects.create(rid=rid, title=detector['check'],
                                                         impact=detector['impact'],
                                                         lines=detector['first_markdown_element'].split("#")[1],
                                                         description=detector['description'])
                        except Exception as e:
                            print(e)
            elif sli_data['success'] is False:
                # sli_status = "failed"
                print(sli_data['error'])
            else:
                sli_info = "Slither has detected the vulnerability.\n"
        else:
            sli_info = "Slither does not detect vulnerabilities.\n"

        # if myth_status == "failed" and sli_status == "failed":
        #     obj = SolAddList.objects.get(id=rid)
        #     obj.status = "failed"
        #     obj.save()
        # result_info = myth_info + "\n" + sli_info
        # return True
    except Exception as e:
        print(e)


# 按钮提交检查
def check_sync_each_file(request):
    rid_get = request.POST.get('rid')
    obj = EtherVerified.objects.get(id=rid_get)
    abs_path = "%s/%s" % (MEDIA_ROOT, obj.fpath)
    version = obj.version
    # obj.runtime = get_bin_file(abs_path, eth_ver=version)
    # 运行检测
    result, check_time = run_file_check(abs_path, eth_ver=version)

    if len(result) > 65535:
        print("Save File")
        filename, extensionname = os.path.splitext(obj.fpath)
        json_file = f"{filename}_result.json"
        report_file = os.path.join(MEDIA_ROOT, json_file)
        # if report_file exist delete
        if os.path.exists(report_file):
            os.remove(report_file)
        # save result
        with open(report_file, "w") as f:
            f.write(result)
            f.flush()
            os.fsync(f.fileno())
        obj.result = json_file
    else:
        obj.result = result
    get_report_json_eth(result, obj.id)
    obj.check_time = check_time
    obj.status = "completed"
    obj.save()
    print("ETH Save Done...")
    return JsonResponse({"res": 1})


def get_sync_report(request):
    global opcode
    rid_get = request.GET.get('rid')
    dcount = 0
    d_list = []
    obj = EtherVerified.objects.get(id=rid_get)
    # 若runtime
    if obj.runtime:
        bincode = obj.runtime
        if bincode[:10] == '0x60806040' or bincode[:8] == '60806040':
            opcode = disassemble_hex(bincode)
    else:
        opcode = ''
    sol_code = get_sol_code_file(obj.fpath)

    if obj.cfg:
        cfg_path = json.loads(obj.cfg)
    else:
        cfg_path = ''

    report_data = {
        'id': obj.id,
        'add': obj.add,
        'name': obj.name,
        'compiler': obj.compiler,
        'version': obj.version,
        'verified_time': obj.verified_time,
        'url': obj.url,
        'fpath': obj.fpath,
        'status': obj.status,
        'result': obj.result,
        'runtime': obj.runtime,
        'opcodes': opcode,
        'sol_code': sol_code,
        'cfg': cfg_path,
    }
    dreport_datas = EtherDeatilList.objects.filter(rid=rid_get)
    for deatillistware in dreport_datas:
        detail_data = {
            'swcid': deatillistware.swcid,
            'title': deatillistware.title,
            'impact': deatillistware.impact,
            'lines': deatillistware.lines,
            'description': deatillistware.description,
        }
        d_list.append(detail_data)
        dcount += 1
    detail = d_list
    return render(request, "get_sync_report.html", {"data": report_data, "detail": detail})
