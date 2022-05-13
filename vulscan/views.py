import json
import logging
import os
import subprocess
import time

import solcx
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from mystery.solidity import get_sol_version, install_solc_version_select
from mytools.platform.ethget import eth_add_parser

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


@login_required
def start_vul_scan(request):
    vulid_get = request.POST.get("vulid")
    obj = SolAddList.objects.get(id=vulid_get)
    try:
        abs_path = "%s/%s" % (settings.MEDIA_ROOT, obj.fpath)
        # 获取Runtime
        obj.runtime = get_bin_file(abs_path)
        # 返回CFG PNG List
        # obj.cfg = get_cfg_png_list(abs_path)
        # 运行检测
        result, check_time = run_file_check(abs_path)
        # 结果保存详细列表
        get_report_json(result, obj.id)
        obj.result, obj.check_time = result, check_time
        obj.status = "completed"
        obj.save()
        print("Save Done...")
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


# Done

def run_file_check(abs_path):
    # obj = SolAddList.objects.get(fpath=sql_path)
    # abs_path = "%s/%s" % (settings.MEDIA_ROOT, obj.fpath)
    global solc_ver
    print("Checking...")
    start = time.perf_counter()
    slither_out = run_slither_check_file(abs_path, 90)
    # print(slither_out)
    print("Slither Done...")
    myth_out = run_myth_check(abs_path, 90)
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
    solc_ver = get_sol_version(file_path)
    if solc_ver is None:
        solc_ver = '0.8.13'
    set_solcx_ver_install(solc_ver)
    # 系统执行命令
    cmd_prefix = f"myth analyze {file_path}"
    myth_out = get_run_command(f"{cmd_prefix} --solv {solc_ver} -o json", timeout)
    return myth_out


def run_slither_check_file(file_path, timeout):
    # 使用Slither分析智能合约源代码
    # 从sol文件中获取合约版本

    ver = get_sol_version(file_path)
    if ver is None:
        ver = '0.8.13'
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
        # print(stdout)
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


def get_bin_file(abs_path):
    global solc_ver
    try:

        solc_ver = get_sol_version(abs_path)
        if solc_ver is None:
            solc_ver = '0.8.13'
        set_solcx_ver_install(solc_ver)
        try:
            out = solcx.compile_files(
                [abs_path],
                output_values=["bin-runtime"],
                solc_version=solc_ver
            )
            for key, value in out.items():
                if len(value['bin-runtime']) > 0 and value['bin-runtime'][:8] == '60806040':
                    # print(value['bin-runtime'])
                    return value['bin-runtime']
                else:
                    return None
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


def get_cfg_png_list(abs_path):
    timeout = 60
    cmd_prefix = f"slither {abs_path}"
    res = subprocess.Popen(f"{cmd_prefix} --print cfg", shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)  # 使用管道
    info_out = res.stdout.readlines()
    # print("CFG Export")
    str_list = [x.decode('utf-8') for x in info_out]
    # 遍历str_list，提取dot文件名
    cfg_png_list = []
    for str_dot in str_list:
        if str_dot.find("dot") != -1:
            png_path = cfg_dot_to_png(str_dot.split(" ")[-1].strip())
            cfg_png_list.append(png_path)
            # 删除dot文件
            if os.path.exists(str_dot.split(" ")[-1].strip()):
                os.remove(str_dot.split(" ")[-1].strip())
    cfg_png_json = json.dumps(cfg_png_list)
    print("CFG Export Done")
    # print(type(cfg_png_json))
    return cfg_png_json


def cfg_dot_to_png(dot_path):
    # 将dot文件转换为png文件
    FileName, ExtensionName = os.path.splitext(dot_path)
    fname = FileName.split('/')[-1]
    dirname = os.path.abspath(os.path.join(FileName, ".."))
    png_fname = f"{fname}.png"
    png_fpath = os.path.join(dirname, png_fname)
    subprocess.check_call(['dot', '-Tpng', f"{dot_path}", '-o', f"{png_fpath}"])
    # 分割png_fpath 保留相对路径
    png_fpath = png_fpath.split('media/')[-1]
    return png_fpath


def set_solcx_ver_install(ver):
    install_list = []
    ver_list = solcx.get_installable_solc_versions()
    for i in ver_list:
        install_list.append(str(i))
    if ver not in install_list:
        print("None")
        solcx.install_solc(ver)
        solcx.set_solc_version(ver)
    else:
        solcx.set_solc_version(ver)
