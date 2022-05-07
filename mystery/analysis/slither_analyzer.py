# 使用Slither分析智能合约源代码，并输出json格式的结果
import json
import logging
import os
import subprocess
import time

from mystery.solidity import *


def _slither_report_json(report_path, all_report_path):
    with open(report_path, 'r', encoding="utf-8") as f:
        dictSlither = json.load(f)
        report_json = {"Slither": dictSlither}

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


def _run_command(cmd, contract_dir, timeout, output):
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
        # subprocess.run(cmd, timeout=timeout, check=True, shell=True, stdout=output)
        # Python3.x中在 Popen() 的args参数运行python时添加 -u 参数，强制python不使用缓冲区
        subprocess.Popen(cmd, shell=True, stdout=output, stderr=subprocess.STDOUT)
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


def run_slither(file_path, timeout):
    # 使用Slither分析智能合约源代码
    # 从sol文件中获取合约版本
    ver = get_sol_version(file_path)
    install_solc_version_select(ver)
    # 获取合约的上级目录路径
    contract_dir = os.path.abspath(os.path.join(file_path, ".."))
    # 获取合约的文件名称，不包含后缀
    contract_name = os.path.basename(file_path).split(".")[0]
    report_path = os.path.join(contract_dir, contract_name + "_slither.json")
    all_report_path = os.path.join(contract_dir, contract_name + "_report.json")
    # print(report_path)
    # 如果存在report.json文件，则删除
    # if os.path.exists(report_path):
    #     os.remove(report_path)

    # 系统执行命令
    cmd_prefix = f"slither {file_path}"

    # 运行slither命令
    _run_command(
        f"{cmd_prefix} --json -",
        contract_dir,
        timeout,
        report_path)

    time.sleep(3)
    _slither_report_json(report_path, all_report_path)
    print("Slither analysis finished.")


# run_slither('/home/hohin/mystery/examples/calls.sol', 60)
