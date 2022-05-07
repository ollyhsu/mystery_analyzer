import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pyevmasm import disassemble_hex, assemble_hex

from mystery_analyzer.settings import MEDIA_ROOT
from .models import EtherVerified
import json
import logging
import os
import sys
import time
from sys import stdin

import requests
from bs4 import BeautifulSoup


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

    # sync_main_code_sql()
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


def insert_ether_data(add, name, compiler, version, verified_time, url):
    # add = request.POST.get("username")
    # name = request.POST.get("username")
    # compiler = request.POST.get("username", None)
    # version = request.POST.get("username", None)
    # verified_time = request.POST.get("username", None)
    # url = request.POST.get("username", None)
    try:

        EtherVerified.objects.create(  # 数据库插入语句
            add=add, name=name, compiler=compiler, version=version, verified_time=verified_time, url=url
        )
        # print("insert success")
        return True
    except:
        # print("data insert error")
        return False


def update_ether_data(add, name, compiler, version, verified_time, url):
    try:
        EtherVerified.objects.filter(add=add, name=name, compiler=compiler, version=version,
                                     verified_time=verified_time, url=url)
        print("update success")
        return True
    except:
        print("data update error")
        return False


# 获取当前时间
def get_now_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S:", time.localtime()), end=' ')
    return 0


def get_sol_code_core_s(each_line):
    filename = each_line['add'] + "-" + each_line['name'] + ".sol"
    save_path = "%s/etherscan/%s" % (MEDIA_ROOT, filename)

    if os.path.exists(save_path):
        get_now_time()
        print(filename + ' 已存在！')
        return 0
    # 伪装成浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.87 Safari/537.36'}
    failed_times = 100
    while True:  # 在制定次数内一直循环，直到访问站点成功

        if failed_times <= 0:
            get_now_time()
            print("失败次数过多，请检查网络环境！")
            break

        failed_times -= 1
        try:
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            get_now_time()
            print('URL: ' + each_line['url'], end='\n')
            response = requests.get(each_line['url'], headers=headers, timeout=5)
            break

        except requests.exceptions.ConnectionError:
            get_now_time()
            print('ConnectionError！请等待3秒！')
            time.sleep(3)

        except requests.exceptions.ChunkedEncodingError:
            get_now_time()
            print('ChunkedEncodingError！请等待3秒！')
            time.sleep(3)

        except:
            get_now_time()
            print('Unfortunitely,出现未知错误！请等待3秒！')
            time.sleep(3)

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, "html.parser")

    targetPRE = soup.find_all('pre', 'js-sourcecopyarea editor')

    with open(save_path, "w+", encoding="utf-8") as fo:
        fo.write(targetPRE[0].text)
        fo.flush()
        os.fsync(fo.fileno())
        fo.close()
        get_now_time()
        print(filename + ' Saved！')

        obj = EtherVerified.objects.get(id=each_line['id'])
        obj.fpath = 'etherscan/%s' % filename
        obj.save()

        # EtherVerified.objects.update(fpath = 'etherscan/%s' % filename)
        # EtherVerified.save()
    return 0


def get_sol_code_s():
    count = 0
    ether_datas_l = EtherVerified.objects.all()[::-1]
    for etherlineware in ether_datas_l:
        ether_data_l = {
            'id': etherlineware.id,
            'add': etherlineware.add,
            'name': etherlineware.name,
            'compiler': etherlineware.compiler,
            'version': etherlineware.version,
            'verified_time': etherlineware.verified_time,
            'url': etherlineware.url,
        }

        # item = ether_data_l.items()
        # key, value = list(item)[1]
        # print(ether_data_l['url'])
        get_sol_code_core_s(ether_data_l)
        count += 1
    print("All Contracts Code Saved.")
    return 0


def get_sol_add_sql(each_url):
    # 伪装成某种浏览器，防止被服务器拒绝服务
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0'}
    # 设置访问网址失败的最高次数，达到制定次数后，报告错误，停止程序
    failed_times = 50

    # 一直循环，直到在制定的次数内访问站点成功
    while True:
        if failed_times <= 0:
            get_now_time()
            print("失败次数过多，请检查网络环境！")
            break

        failed_times -= 1  # 每执行一次就要减1
        try:
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            print('URL: ' + each_url)

            response = requests.get(url=each_url, headers=headers, timeout=5)

            # 执行到这一句意味着成功访问，于是退出while循环
            break
        except requests.exceptions.ConnectionError:
            get_now_time()
            print('ConnectionError!请等待3秒！')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            get_now_time()
            print('ChunkedEncodingError!请等待3秒！')
            time.sleep(3)
        except:
            get_now_time()
            print('出现未知错误！请等待3秒！')
            time.sleep(3)

    # 转换成UTF-8编码
    response.encoding = response.apparent_encoding

    # 煲汤
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找这个字段，这个字段下，包含智能合约代码的URL地址
    targetDiv = soup.find_all('div', 'table-responsive mb-2 mb-md-0')

    try:
        targetTBody = targetDiv[0].table.tbody
    except:
        get_now_time()
        print("targetTBody未成功获取！")
        return 1

    for targetTR in targetTBody:
        if targetTR.name == 'tr':
            col = targetTR.find_all('td')
            # 暂只支持Solidity语法的合约代码
            if col[2].text == 'Solidity':
                add = targetTR.td.find('a', 'hash-tag text-truncate').attrs['title']
                name = col[1].text
                compiler = col[2].text
                version = str(col[3].text).strip()
                verified_time = col[7].text
                url = "https://etherscan.io" + targetTR.td.find('a', 'hash-tag text-truncate').attrs['href']
                insert_ether_data(add, name, compiler, version, verified_time, url)
    return 0


def update_url_sql():
    urlList = ["https://etherscan.io/contractsVerified/1?ps=100",
               "https://etherscan.io/contractsVerified/2?ps=100",
               "https://etherscan.io/contractsVerified/3?ps=100",
               "https://etherscan.io/contractsVerified/4?ps=100",
               "https://etherscan.io/contractsVerified/5?ps=100"]

    # 读取urlList里的每一个URL网页里的智能合约地址
    for each_url in urlList:
        wait_time = 0
        while 1 == get_sol_add_sql(each_url):
            wait_time += 1
            if wait_time == 10:
                break
            pass

    # 函数正常执行，返回0
    return 0


# 同步Mainnet合约代码
def sync_main_code_sql():
    # 根据智能合约的地址去爬取智能合约的代码
    get_sol_code_s()
    print("saved success")
