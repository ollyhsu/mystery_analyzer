"""
从.data/report目录下获取漏洞检测报告
"""

import os
from mystery.utils import get_logger

logger = get_logger(__name__)

root_dir = os.getcwd()  # /home/hohin/mystery
report_dir = os.path.join(root_dir, ".data/report/")


def handle_report_path(path):
    """
    处理报告路径,以-分割文件名和文件夹名
    """
    FileName_path, ExtensionName = os.path.splitext(path)
    report_id = FileName_path.split("_")[0].split("/")[-1]
    address = FileName_path.split("_")[-1]
    return report_id, address


def get_report_txt(re_path):
    """
    获取漏洞检测报告
    """
    if not os.path.exists(re_path):
        logger.error("report_path: %s not exists", re_path)
        return

    with open(re_path, 'r') as f:
        report_txt = f.read()
    return report_txt


def get_report_by_id(report_id_user):
    """
    通过report_id从report_dir目录下获取漏洞检测报告
    """
    # 循环遍历report_dir目录下的所有文件，找到report_id开头对应的文件
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file.startswith(report_id_user):
                rep_path = os.path.join(root, file)
                return rep_path


def get_report_by_address(address):
    """
    通过address从report_dir目录下获取漏洞检测报告
    """
    # 循环遍历report_dir目录下的所有文件，找到address开头对应的文件
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            file_name = file.split("_")[-1]
            file_add = file_name.split("-")[0]
            # print(file_add)
            if file_add.startswith(address):
                rep_path = os.path.join(root, file)
                return rep_path


def get_report_id_txt(report_id):
    """
    通过report_id获取漏洞检测报告
    """
    report_path = get_report_by_id(report_id)
    if report_path is None:
        print(f"report_id: {report_id} not exists")
    else:
        print("-------------Result---------------")
        print(get_report_txt(report_path))
        print("---------------END----------------")


def get_report_address_txt(address):
    """
    通过address获取漏洞检测报告
    """
    report_path = get_report_by_address(address)
    if report_path is None:
        print(f"address: {address} not exists")
    else:
        print("-------------Result---------------")
        print(get_report_txt(report_path))
        print("---------------END----------------")

# print(get_report_address_txt("0x1351161"))
