"""
使用mythril工具进行漏洞分析，并返回json格式的结果
"""
import json
import logging
import os
import subprocess

from mystery.solidity import *


def _myth_report_json(report_path, all_report_path):
    """
    Parse the myth report json file.
    """
    with open(report_path, 'r', encoding="utf-8") as f:
        dictSlither = json.load(f)
        report_json = {"Mythril": dictSlither}

    # print(report_json)
    # 如果文件不存在，则创建report文件
    if not os.path.exists(all_report_path):
        with open(all_report_path, 'w', encoding="utf-8") as f:
            f.write('{}')
    # 将report_json写入all_report_path
    with open(all_report_path, 'r', encoding="utf-8") as f:
        dictAll = json.load(f)
        # dictAll[contract_name] = report_json
        dictAll.update(report_json)
    with open(all_report_path, 'w', encoding="utf-8") as f:
        json.dump(dictAll, f, ensure_ascii=False)

    # 执行完毕后，删除report_path
    os.remove(report_path)


def _run_command(cmd, contract_dir, timeout, output=None):
    """
    Run a command and return the output.
    """
    cwd = os.getcwd()
    os.chdir(contract_dir)
    if output is not None:
        output = open(output, "w")
    else:
        output = open("/dev/null", "w")
    try:
        logging.debug(f"execute cmd: {cmd}")
        subprocess.run(cmd, timeout=timeout, check=True,
                       stdout=output, shell=True)
        return True
    except subprocess.TimeoutExpired as e:
        logging.warning(
            f"[execute_command]timeout occurs when running `{cmd}`, timeout: {timeout}s")
        return False
    except Exception as e:
        logging.warning(
            f"[execute_command]error occurs when running `{cmd}`, output: {e}")
        return False
    finally:
        output.close()
        os.chdir(cwd)


def run_myth(file_path, timeout):
    """
    Run the myth analysis tool on the input file.
    """
    # Mythril 不支持自动检测合约版本，需要手动指定合约版本
    # 从sol文件中获取合约版本
    ver = get_sol_version(file_path)
    # 获取合约的上级目录路径
    contract_dir = os.path.abspath(os.path.join(file_path, ".."))
    # 获取合约的文件名称，不包含后缀
    contract_name = os.path.basename(file_path).split(".")[0]
    report_path = os.path.join(contract_dir, contract_name + "_myth.json")
    all_report_path = os.path.join(contract_dir, contract_name + "_report.json")

    # 系统执行命令
    cmd_prefix = f"myth analyze {file_path}"
    _run_command(
        f"{cmd_prefix} --solv {ver} -o json",
        contract_dir,
        timeout,
        report_path)
    # 处理Myth执行结果
    _myth_report_json(report_path, all_report_path)
    print("Mythril analysis finished.")


# run_myth('/home/hohin/mystery/examples/calls.sol', 60)

