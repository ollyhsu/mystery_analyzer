import json
import logging
import os
import sys
import time
from sys import stdin

import requests
from bs4 import BeautifulSoup

logging.basicConfig()
logger = logging.getLogger("Mystery")

root_dir = os.getcwd()  # /home/hohin/mystery
add_path = os.path.join(root_dir, ".data/etherscan/")
code_path = os.path.join(root_dir, ".data/etherscan/code/")
code_tmp = os.path.join(root_dir, ".data/etherscan/tmp/")

# 获取当前时间
def get_now_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S:", time.localtime()), end=' ')
    return 0


# 获取runtime字节码
def get_runtime_core(each_line):
    pass


# 获取sol合约代码核心文件
def get_sol_code_core(each_line):
    sc_add = each_line[0]
    # print(sc_add)
    if os.path.exists(code_path + sc_add + "-" + each_line[1] + '.sol'):
        get_now_time()
        print(sc_add + "-" + each_line[1] + ' 已存在！')
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
            print('URL: ' + each_line[5], end='')
            response = requests.get(each_line[5], headers=headers, timeout=5)
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

    with open(code_path + sc_add + "-" + each_line[1] + '.sol', "w+", encoding="utf-8") as fo:
        fo.write(targetPRE[0].text)
        fo.flush()
        os.fsync(fo.fileno())
        fo.close()
        get_now_time()
        print(sc_add + "-" + each_line[1] + ' Saved！')

    return 0


def get_sol_code():
    add_file = os.path.join(add_path, "address.txt")
    with open(add_file, 'r') as f:
        while True:
            lines = f.readline()
            cline = lines.split(",")
            if not lines:
                break
            # print(cline[1])
            get_sol_code_core(cline)  # 核心函数
    print("All Contracts Code Saved.")
    return 0


# 更新URL
def get_sol_add(each_url):
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

    # 以追加的方式打开文件。
    # 如果文件不存在，则新建；如果文件已存在，则在文件指针末尾追加
    add_list = []
    with open(add_path + "address.txt", "a") as fo:
        # 把每一个地址，都写到文件里面保存下来
        for targetTR in targetTBody:
            if targetTR.name == 'tr':
                col = targetTR.find_all('td')
                # 暂只支持Solidity语法的合约代码
                if col[2].text == 'Solidity':
                    fo.write(targetTR.td.find('a', 'hash-tag text-truncate').attrs['title'] + ","
                             + col[1].text + ","
                             + col[2].text + ","
                             + col[3].text + ","
                             + col[7].text + ","
                             + "https://etherscan.io" + targetTR.td.find('a', 'hash-tag text-truncate').attrs[
                                 'href'] + "\n")
        fo.flush()
        os.fsync(fo.fileno())
        fo.close()
    return 0


def update_url():
    urlList = ["https://etherscan.io/contractsVerified/1?ps=100",
               "https://etherscan.io/contractsVerified/2?ps=100",
               "https://etherscan.io/contractsVerified/3?ps=100",
               "https://etherscan.io/contractsVerified/4?ps=100",
               "https://etherscan.io/contractsVerified/5?ps=100"]

    # 把旧的存放合约地址的文件清除干净
    try:
        if os.path.exists(add_path + "address.txt"):
            os.remove(add_path + "address.txt")
            get_now_time()
            print('已清除%s目录下的旧文件（仓库）！' % add_path)
    except IOError:
        get_now_time()
        print("出现一个不能处理的错误，终止程序：IOError!")
        # 函数不正常执行，返回1
        return 1

    # 读取urlList里的每一个URL网页里的智能合约地址
    for each_url in urlList:
        wait_time = 0
        while 1 == get_sol_add(each_url):
            wait_time += 1
            if wait_time == 10:
                break
            pass

    # 函数正常执行，返回0
    return 0


# 同步Mainnet合约代码
def sync_mainnet_code():
    # 用于将Python解释器堆栈的最大深度设置为所需的限制
    # 此限制可防止任何程序进入无限递归，否则无限递归将导致C堆栈溢出并使Python崩溃
    sys.setrecursionlimit(1500)
    if os.path.exists(add_path + "address.txt"):
        print('是否更新智能合约地址库？Y/y开始更新:')
        input_string = str(stdin.readline())

        if (input_string[0] == 'Y') | (input_string[0] == 'y'):
            print('开始更新智能合约地址库:')
            update_url()
    else:
        print('开始新建智能合约地址库:')
        update_url()

    # 根据智能合约的地址去爬取智能合约的代码
    get_sol_code()


# 获取sol合约代码核心文件
def get_sol_code_m(each_add):
    each_add_url = "https://etherscan.io/address/%s#code" % each_add
    print(each_add_url)
    if os.path.exists(code_tmp + each_add + '.sol'):
        get_now_time()
        print(code_tmp + each_add + ' 已存在！')
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
            print('URL: ' + each_add_url, end='\n')
            response = requests.get(each_add_url, headers=headers, timeout=5)
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

    with open(code_tmp + each_add + '.sol', "w+", encoding="utf-8") as fo:
        fo.write(targetPRE[0].text)
        fo.flush()
        os.fsync(fo.fileno())
        fo.close()
        get_now_time()
        print(each_add + ' Saved！')

    return 0


# 解析Etherscan地址
def eth_add_parser(eth_add):
    try:
        get_sol_code_m(eth_add)
        print("Parser Success.")
    except FileNotFoundError as e:
        print(e)
