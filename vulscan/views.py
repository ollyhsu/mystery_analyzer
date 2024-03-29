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
from mystery_analyzer.settings import MEDIA_ROOT
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
        obj.cfg = get_cfg_png_list(abs_path)
        # 运行检测
        result, check_time = run_file_check(abs_path)
        if len(result) > 65535:
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
        # 结果保存详细列表
        get_report_json(result, obj.id)
        obj.check_time = check_time
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

def run_file_check(abs_path, **kwargs):
    solcv_check_kwargs = ''
    if kwargs:
        for key, value in kwargs.items():
            if key == 'eth_ver':
                solcv_check_kwargs = value
        # print(solcv_check_kwargs)
    else:
        print("run_file_check not kwargs")
    # obj = SolAddList.objects.get(fpath=sql_path)
    # abs_path = "%s/%s" % (settings.MEDIA_ROOT, obj.fpath)
    print("Checking...")
    start = time.perf_counter()
    slither_out = run_slither_check_file(abs_path, 90, solcv_check_kwargs)
    print("Slither Done...")
    myth_out = run_myth_check(abs_path, 90, solcv_check_kwargs)
    print("Mthril Done...")
    if slither_out == "timeout":
        slither_out = '''{"success": false, "error": "Error: slither execution timed out", "results": {}}'''
    if slither_out == "failed":
        slither_out = '''{"success": false, "error": "Error: slither check failed", "results": {}}'''
    if myth_out == "timeout":
        myth_out = '''{"success": false, "error": "Error: mythril execution timed out", "issues": []}'''
    if myth_out == "failed":
        myth_out = '''{"success": false, "error": "Error: mythril check failed", "issues": []}'''
    end = time.perf_counter()
    check_time = "%.2f" % (end - start)
    # 将myth_out和slither_out嵌套到一个json中
    sdict = json.loads(slither_out)
    mdict = json.loads(myth_out)
    result_dict = [{"Mythril": mdict}, {"Slither": sdict}]
    result_json = json.dumps(result_dict)
    print("Check Done...")
    # print(len(result_json))
    return result_json, check_time


def run_myth_check(file_path, timeout, solcv_kwargs):
    """
    Run the myth analysis tool on the input file.
    """
    # Mythril 不支持自动检测合约版本，需要手动指定合约版本
    # 从sol文件中获取合约版本
    # print(solcv_kwargs)
    if solcv_kwargs:
        print("myth has kwargs")
        solc_ver_myth = solcv_kwargs
    else:
        print("myth not kwargs")
        solc_ver_bin = get_sol_version(file_path)
        # print(solc_ver_bin)
        if solc_ver_bin is None:
            solc_ver_myth = '0.8.13'
        else:
            solc_ver_myth = solc_ver_bin
    set_solcx_ver_install(solc_ver_myth)
    # 系统执行命令
    cmd_prefix = f"myth analyze {file_path}"
    myth_out = get_run_command(f"{cmd_prefix} --solv {solc_ver_myth} -o json", timeout)
    return myth_out


def run_slither_check_file(file_path, timeout, solcvs_kwargs):
    # 使用Slither分析智能合约源代码
    # 从sol文件中获取合约版本
    if solcvs_kwargs:
        print("slither has kwargs")
        solc_ver_sli = solcvs_kwargs
    else:
        print("slither not kwargs")
        solc_ver_bin = get_sol_version(file_path)
        # print(solc_ver_bin)
        if solc_ver_bin is None:
            solc_ver_sli = '0.8.13'
        else:
            solc_ver_sli = solc_ver_bin
    # set_solcx_ver_install(solc_ver_sli)
    install_solc_version_select(solc_ver_sli)
    # 系统执行命令
    cmd_prefix = f"slither {file_path}"
    slither_out = get_run_command(f"{cmd_prefix} --json -", timeout)
    return slither_out


def get_run_command(cmd, timeout):
    """
    Run a command and return the output.
    """
    logging.debug(f"execute cmd: {cmd}")
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    try:
        if p.poll() is not None:
            print(p.poll())
            print("the popen not run, restart this:%s" % cmd)
            # pipe = sp.Popen(command, stdin=sp.PIPE, env=my_env)
            time.sleep(10)
        # print(stdout)
        stdout, stderr = p.communicate(timeout=timeout)
        out = stdout.decode('utf-8')
        return out

    except subprocess.TimeoutExpired as e:
        logging.warning(
            f"[execute_command]timeout occurs when running `{cmd}`, timeout: {timeout}s")
        p.kill()
        return "timeout"
    except Exception as e:
        logging.warning(
            f"[execute_command]error occurs when running `{cmd}`, output: {e}")
        return "failed"


def get_bin_file(abs_path, **kwargs):
    # print(abs_path, kwargs)
    solc_ver_runtime = ''
    try:
        if kwargs:
            print("get_bin has kwargs")
            for key, value in kwargs.items():
                if key == 'eth_ver':
                    solc_ver_runtime = value
        else:
            print("get_bin not kwargs")
            solc_ver_bin = get_sol_version(abs_path)
            # print(solc_ver_bin)
            if solc_ver_bin is None:
                solc_ver_runtime = '0.8.13'
            else:
                solc_ver_runtime = solc_ver_bin
        set_solcx_ver_install(solc_ver_runtime)
        try:
            out = solcx.compile_files(
                [abs_path],
                output_values=["bin-runtime"],
                solc_version=solc_ver_runtime
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
    # print(abs_path)
    cmd_prefix = f"slither {abs_path}"
    res = subprocess.Popen(f"{cmd_prefix} --print cfg", shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)  # 使用管道
    try:
        info_out = res.stdout.readlines()
        print("CFG Export")
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
        # 刷新缓冲区
        res.stdout.flush()
        print("CFG Export Done")
        # print(type(cfg_png_json))
        return cfg_png_json
    except Exception as e:
        res.kill()
        return False


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
        try:
            solcx.set_solc_version(ver)
        except solcx.exceptions.SolcNotInstalled:
            solcx.install_solc(ver)
            solcx.set_solc_version(ver)
    else:
        try:
            solcx.set_solc_version(ver)
        except solcx.exceptions.SolcNotInstalled:
            solcx.install_solc(ver)
            solcx.set_solc_version(ver)
