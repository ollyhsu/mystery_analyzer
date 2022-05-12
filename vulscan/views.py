import json
import logging
import os
import subprocess
import time

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from mystery.solidity import get_sol_version, install_solc_version_select
from mytools.views import eth_add_parser
from vulreport.views import get_report_json
from vulscan.models import SolAddList


# Create your views here.
@login_required
def vulscan(request):
    return render(request, "vulscan.html")


@login_required
def sol_upload_handle(request):
    try:
        stime = time.time()
        '''sol上传处理页'''
        # sol = request.FILES.get('upload_file').read()
        # sol = request.FILES['upload_file']
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
        sql_path = 'file_upload/%s' % tname

        # 【4】保存路径到数据库，此处只保存其相对上传目录的路径
        SolAddList.objects.create(fname=sol.name, fpath=sql_path, scantype="file", time=int(stime),
                                  uid=request.user.id, status="running")
        obj = SolAddList.objects.get(fpath=sql_path)
        # 【5】别忘记返回信息
        return JsonResponse({"res": 1, "id": obj.id})
    except Exception as e:
        return JsonResponse({"res": 0})


def run_file_check(sql_path):
    obj = SolAddList.objects.get(fpath=sql_path)
    abs_path = "%s/%s" % (settings.MEDIA_ROOT, obj.fpath)
    print("Checking...")
    start = time.perf_counter()
    slither_out = run_slither_check_file(abs_path, 60)
    # print(slither_out)
    print("Slither Done...")
    myth_out = run_myth_check(abs_path, 60)
    print("Mthril Done...")
    end = time.perf_counter()
    check_time = "%.2f" % (end - start)
    # 将myth_out和slither_out嵌套到一个json中
    sdict = json.loads(slither_out)
    mdict = json.loads(myth_out)
    result_dict = [{"Mythril": mdict}, {"Slither": sdict}]
    result_json = json.dumps(result_dict)
    print("Done...")
    return result_json, check_time


def run_myth_check(file_path, timeout):
    """
    Run the myth analysis tool on the input file.
    """
    # Mythril 不支持自动检测合约版本，需要手动指定合约版本
    # 从sol文件中获取合约版本
    ver = get_sol_version(file_path)
    # 系统执行命令
    cmd_prefix = f"myth analyze {file_path}"
    myth_out = get_run_command(f"{cmd_prefix} --solv {ver} -o json", timeout)
    return myth_out


def run_slither_check_file(file_path, timeout):
    # 使用Slither分析智能合约源代码
    # 从sol文件中获取合约版本
    ver = get_sol_version(file_path)
    if ver is None:
        slither_out = '''{"success": false, "error": "Cannot Find Sol version", "results": {}}'''
        return slither_out
    else:
        install_solc_version_select(ver)
        # 系统执行命令
        cmd_prefix = f"slither {file_path}"
        slither_out = get_run_command(f"{cmd_prefix} --json -", timeout)
        return slither_out


def get_run_command(cmd, timeout):
    """
    Run a command and return the output.
    """
    try:
        logging.debug(f"execute cmd: {cmd}")
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
        stdout, stderr = p.communicate(timeout=timeout)
        out = stdout.decode('utf-8')
        return out
    except subprocess.TimeoutExpired as e:
        logging.warning(
            f"[execute_command]timeout occurs when running `{cmd}`, timeout: {timeout}s")
        return False
    except Exception as e:
        logging.warning(
            f"[execute_command]error occurs when running `{cmd}`, output: {e}")
        return False


@login_required
def start_vul_scan(request):
    vulid_get = request.POST.get("vulid")
    obj = SolAddList.objects.get(id=vulid_get)
    try:
        sql_path = obj.fpath
        result, check_time = run_file_check(sql_path)
        obj.result = result
        obj.status = "completed"
        obj.check_time = check_time
        obj.save()
        get_report_json(result, obj.id)
        return JsonResponse({"res": 1})
    except Exception as e:
        return JsonResponse({"res": 0})


@login_required
def ether_add_handle(request):
    try:
        stime = time.time()
        ether_add = request.POST.get("ether_add")
        if ether_add[:2] == '0x':
            tname = "%s-%s.sol" % (ether_add, int(stime))
            add_path = "%s/eth_add/%s" % (settings.MEDIA_ROOT, tname)
            eth_add_parser(ether_add, add_path)
            s_path = "eth_add/%s" % tname
            # 【4】保存路径到数据库，此处只保存其相对上传目录的路径
            SolAddList.objects.create(add=ether_add, fpath=s_path, scantype="add", time=int(stime),
                                      uid=request.user.id, status="running")
            obj = SolAddList.objects.get(fpath=s_path)
            return JsonResponse({"res": 1, "id": obj.id})
        else:
            return JsonResponse({"res": 0})
    except Exception as e:
        return JsonResponse({"res": 0})
