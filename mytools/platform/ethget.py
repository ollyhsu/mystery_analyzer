import os
import time

import requests
from bs4 import BeautifulSoup

from mystery_analyzer import settings
from mytools.models import EtherVerified


def insert_ether_data(add, name, compiler, version, verified_time, url):
    try:

        EtherVerified.objects.create(  # 数据库插入语句
            add=add, name=name, compiler=compiler, version=version, verified_time=verified_time, url=url,
            status="running"
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
    if not os.path.isdir("%s/etherscan" % settings.MEDIA_ROOT):
        os.makedirs("%s/etherscan" % settings.MEDIA_ROOT)
    save_path = "%s/etherscan/%s" % (settings.MEDIA_ROOT, filename)

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


# 获取sol合约代码核心文件
def get_sol_code_m(each_add, add_path):
    each_add_url = "https://etherscan.io/address/%s#code" % each_add
    # print(each_add_url)

    if not os.path.isdir("%s/eth_add" % settings.MEDIA_ROOT):
        os.makedirs("%s/eth_add" % settings.MEDIA_ROOT)

    # file_name, extension_name = os.path.splitext(sol.name)
    # tname = "%s-%s.sol" % (each_add, int(stime))
    # add_path = "%s/eth_add/%s" % (settings.MEDIA_ROOT, tname)

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

    with open(add_path, "w+", encoding="utf-8") as fo:
        fo.write(targetPRE[0].text)
        fo.flush()
        os.fsync(fo.fileno())
        fo.close()
        get_now_time()
        print('Saved！')

    # with open(code_tmp + each_add + '.sol', "w+", encoding="utf-8") as fo:
    #     fo.write(targetPRE[0].text)
    #     fo.flush()
    #     os.fsync(fo.fileno())
    #     fo.close()
    #     get_now_time()
    #     print(each_add + ' Saved！')

    return 0


# 解析Etherscan地址
def eth_add_parser(eth_add, addpath):
    try:
        get_sol_code_m(eth_add, addpath)
        print("Parser Success.")
    except FileNotFoundError as e:
        print(e)
