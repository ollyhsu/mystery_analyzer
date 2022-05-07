import os
import sys
import time
from subprocess import check_call
from evm_cfg_builder.cfg import CFG
from tqdm import tqdm
# Done

# 根据字节码构建控制流程图
from mystery.compiler import get_sol_bytecode


def build_cfg_graph(fname):
    # print(fname)
    FileName, ExtensionName = os.path.splitext(fname)
    if ExtensionName in ['.bin', '.bin-runtime']:
        with open(fname, encoding="utf8") as bytecode_file:
            byte_code = bytecode_file.read()
            if byte_code[:10] == '0x60806040':
                cfg = CFG(byte_code)
                CFG.output_to_dot(cfg, f"{FileName}-")
                # 利用子进程将dot文件转换成png格式
                check_call(['dot', '-Tpng', f"{FileName}-FULL_GRAPH.dot", '-o', f"{FileName}-FULL_GRAPH.png"])
                # 清空系统缓冲区
                sys.stdout.flush()
                # 进度条 10s
                for i in tqdm(range(100)):
                    time.sleep(0.1)
            elif byte_code[:8] == '60806040':
                cfg = CFG("0x" + byte_code)
                CFG.output_to_dot(cfg, f"{FileName}-")
                # 利用子进程将dot文件转换成png格式
                check_call(['dot', '-Tpng', f"{FileName}-FULL_GRAPH.dot", '-o', f"{FileName}-FULL_GRAPH.png"])
                # 清空系统缓冲区
                sys.stdout.flush()
                # 进度条 10s
                for i in tqdm(range(100)):
                    time.sleep(0.1)
            else:
                print("Invalid ByteCode.")
    elif ExtensionName in ['.sol']:
        bytecode = get_sol_bytecode(fname)
        cfg = CFG("0x" + bytecode)
        CFG.output_to_dot(cfg, f"{FileName}-")
        # 利用子进程将dot文件转换成png格式
        check_call(['dot', '-Tpng', f"{FileName}-FULL_GRAPH.dot", '-o', f"{FileName}-FULL_GRAPH.png"])
        # 清空系统缓冲区
        sys.stdout.flush()
        # 进度条 10s
        for i in tqdm(range(100)):
            time.sleep(0.1)
    else:
        print("Invalid *.bin-runtime/*.sol File.")
