import solcx
import os
import re
from jsonpath import jsonpath

# Done

#  正则匹配 solidity版本
PATTERN = re.compile(r"pragma solidity\s*(?:\^|>=|<=)?\s*(\d+\.\d+\.\d+)")


# 获取solc版本
def _search_solc(target: str):
    with open(target, encoding="utf8") as file_desc:
        buf = file_desc.read()
        return PATTERN.findall(buf)  # e.g. 0.4.25


# 编译 bytecode
def _sol_compile(sol_fname):
    try:
        # solc_ver = str(_search_solc(sol_fname))[2:-2]
        solc_v = _search_solc(sol_fname)
        solc_ver = max(solc_v)
        try:
            plist = os.path.splitext(sol_fname)
            out = solcx.compile_files(
                [sol_fname],
                output_values=["bin-runtime"],
                solc_version=solc_ver
            )
            # print(out)
            # out_bin_runtime = jsonpath(out, "$..bin-runtime")
            # out_bin_json = json.dumps(out)
            for key, value in out.items():
                # print(key, "|", value['bin-runtime'])
                l_name = key.split(":")
                # print(l_name[-1])
                # print(value['bin-runtime'])
                if len(value['bin-runtime']) > 0:
                    with open(f"{plist[0]}-{l_name[-1]}.bin-runtime", "wb", buffering=0) as f:
                        f.write(bytes(value['bin-runtime'], encoding='utf8'))
                        f.flush()
                        os.fsync(f.fileno())
            print("Saved Success.")

        except solcx.exceptions.SolcNotInstalled:
            print("Solc v" + solc_ver + " Not installed.\nInstalling...")
            solcx.install_solc(solc_ver)
            print("Solc v" + solc_ver + " installed.")
            _sol_compile(sol_fname)
    except FileNotFoundError:
        print("Sol File Not Found")


# 编译单独或文件夹下sol文件
def sol_to_runtime(sol_path):
    try:
        if os.path.isfile(sol_path):
            # 直接编译单独的sol文件
            _sol_compile(sol_path)
        elif os.path.isdir(sol_path):
            # 读入文件夹
            files1 = os.listdir(sol_path)
            # 统计一级文件夹中的二级文件夹个数
            num1 = len(files1)
            for i in range(num1):
                dlist = os.path.splitext(files1[i])
                if dlist[1] in ['.sol']:
                    print("Filename: " + files1[i])
                    signal_fpath = sol_path + '//' + files1[i]
                    _sol_compile(signal_fpath)
        else:
            print("Please enter a valid file or directory path.")
    except FileNotFoundError:
        print("Sol File Not Found")


# 返回bin-runtime
def get_sol_bytecode(sol_fname):
    try:
        # solc_ver = str(_search_solc(sol_fname))[2:-2]
        solc_v = _search_solc(sol_fname)
        solc_ver = max(solc_v)
        try:
            out = solcx.compile_files(
                [sol_fname],
                output_values=["bin-runtime"],
                solc_version=solc_ver
            )
            # out_bin_runtime = jsonpath(out, "$..bin-runtime")
            # out_bin = str(out_bin_runtime)[2:-2]
            # return out_bin
            len_bin = 0
            for key, value in out.items():
                # print(key, "|", value['bin-runtime'])
                l_name = key.split(":")
                # print(l_name[-1])
                # print(value['bin-runtime'])
                if len(value['bin-runtime']) > 0 and value['bin-runtime'][:8] == '60806040' :
                    return value['bin-runtime']
        except solcx.exceptions.SolcNotInstalled:
            print("Solc v" + solc_ver + " Not installed.")
            solcx.install_solc(solc_ver)
            print("Solc v" + solc_ver + " installed.")
            _sol_compile(sol_fname)
    except FileNotFoundError:
        print("Sol File Not Found")
