import os
import sys
from subprocess import check_call

from slither.slither import Slither
from mystery.solidity.get_sol_version import get_sol_version
from mystery.solidity.solc_install import install_solc_version_select


# 基于Slither API 创建函数调用关系图，输出为dot格式
def export_dot_to_png(dot_fname):
    # 将dot文件转换为png文件
    FileName, ExtensionName = os.path.splitext(dot_fname)
    fname = FileName.split('/')[-1]
    dirname = os.path.abspath(os.path.join(FileName, ".."))
    png_fname = f"{fname}.png"
    png_fpath = os.path.join(dirname, png_fname)
    # print(f"Export {png_fpath}")
    check_call(['dot', '-Tpng', f"{dot_fname}", '-o', f"{png_fpath}"])


def export_call_graph(sol_fname):
    # 从sol文件中获取合约版本号
    ver = get_sol_version(sol_fname)
    # 切换到solc版本
    install_solc_version_select(ver)

    FileName, ExtensionName = os.path.splitext(sol_fname)
    fname = FileName.split('/')[-1]
    # Init slither
    slither = Slither(sol_fname)
    # Get the call graph
    for contract in slither.contracts:
        for function in contract.functions + contract.modifiers:
            # 创建Filename的空文件夹
            if not os.path.exists(FileName):
                os.makedirs(FileName)
            call_path = os.path.join(FileName, fname)
            # print(call_path)
            sol_fname = f"{call_path}-{contract.name}-{function.full_name}.dot"
            # print(f"Export {sol_fname}")
            function.slithir_cfg_to_dot(sol_fname)
            # print("Export call graph to dot file Successfully!")
    # 循环遍历FileName目录下的所有dot文件，并转换为png文件
    for file in os.listdir(FileName):
        if file.endswith(".dot"):
            # print(os.path.join(FileName, file))
            export_dot_to_png(os.path.join(FileName, file))
    print("Export dot to png Successfully!")
    sys.stdout.flush()
