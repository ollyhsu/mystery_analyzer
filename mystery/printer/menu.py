import sys

from mystery.analysis.loader import run_analysis_tools
from mystery.compiler import *
from mystery.solidity import *
from mystery.utils import *


def _logo():
    print("----------------------------------")
    print(" Mystery Solidity Analyzer v1.0.0 ")


# 实用工具箱菜单

def toolbox():
    while True:
        print("-----——------Toolbox---——--------—")
        print(" [a] *.sol to EVM Runtime")
        print(" [b] EVM Runtime to Opcodes")
        print(" [c] *.sol to Opcodes")
        print(" [d] Opcodes to Runtime")
        print(" [e] Draw Call Graph")
        print(" [f] Manually install solc-version")
        print(" [g] Etherscan Address Parser")
        print(" [q] Back to pre-menu")
        print("----------------------------------")
        cho = input("Please input choose:")
        # *.sol to EVM Runtime
        if cho == 'a' or cho == 'A':
            sol_path = input("Please Enter *.sol File/Directory Path:")
            sol_to_runtime(sol_path)
        # EVM Runtime to Opcodes
        elif cho == 'b' or cho == 'B':
            byte_path = input("Please Enter *.bin-runtime File/Directory Path or Bytecode:")
            evm_to_opcode(byte_path)
        # *.sol to Opcodes
        elif cho == 'c' or cho == 'C':
            sol_path = input("Please Enter *.sol File/Directory Path:")
            sol_to_opcode(sol_path)
        # Opcodes to Runtime
        elif cho == 'd' or cho == 'D':
            op_path = input("Please Enter *.opcode File/Directory Path:")
            opcode_to_bin(op_path)
        # Draw EVM CFG
        elif cho == 'e' or cho == 'E':
            cfg_path = input("Please Enter *.bin-runtime or *.sol File/Directory Path:")
            export_call_graph(cfg_path)
        # Manually install solc-version
        elif cho == 'f' or cho == 'F':
            solc_ver = input("Please enter Solc Ver (e.g. 0.4.25) or *.sol Path:")
            install_solcv(solc_ver)
        elif cho == 'g' or cho == 'G':
            eth_add = input("Please enter Add (e.g. 0x0db3b4acf7819df4699f0b6b6390962556e17f2c):")
            eth_add_parser(eth_add)
        # Back to pre-menu
        elif cho == 'q' or cho == 'Q':
            break
        else:
            print("Input Error")
            continue


# 漏洞检测模块菜单

def concolic_analyzer():
    pass


# 将EVM汇编码处理成SVM汇编码
def evm_to_svm(bytecode):
    pass


def static_analyzer():
    pass


def vul_detection():
    while True:
        print("-----—----VUL Detection---—-—----—")
        print(" [a] Sol Detection")
        print(" [b] Ethereum Address Detection")
        print("----------------------------------")
        cho = input("Please input choose:")
        # 自动综合分析模块
        if cho == 'a' or cho == 'A':
            solname = input("Please Enter *.sol Path:")
            # run_analysis_tools('/home/hohin/mystery/examples/calls.sol', 60)
            run_analysis_tools(solname, 60)
            break
        # 静态分析模块
        elif cho == 'b' or cho == 'B':
            print("Please Enter EVM Runtime")
            static_analyzer()
            break
        # 符号执行模块
        elif cho == 'c' or cho == 'C':
            concolic_analyzer()
            break
        elif cho == 'q' or cho == 'Q':
            break  # 返回上一菜单
        else:
            print("Input Error")


# 漏洞检测结果查询
def result_query():
    while True:
        print("-----—----VUL Detection---—-—----—")
        print(" [a] Select All Results")
        print(" [b] Select Result by Report ID")
        print(" [c] Select Result by ETH Address")
        print(" [q] Back to pre-menu")
        print("----------------------------------")
        cho = input("Please input choose:")
        if cho == 'a' or cho == 'A':
            print("Please Enter *.sol Path")
            break
        elif cho == 'b' or cho == 'B':
            reportid = input("Please VUl Detection Report ID:")
            get_report_id_txt(reportid)
        elif cho == 'c' or cho == 'C':
            reportadd = input("Please ETH Address:")
            get_report_address_txt(reportadd)
        elif cho == 'q' or cho == 'Q':
            break  # 返回上一菜单
        else:
            print("Input Error")


# 管理菜单
def admin_panel():
    while True:
        print("-----—-----Admin Panel----—-—----—")
        print(" [a] SQL Test")
        print(" [b] Sync Etherscan mainnet code")
        print(" [c] Delete Report by ID")
        print(" [d] Clean Data")
        print(" [q] Back to pre-menu")
        print("----------------------------------")
        cho = input("Please input choose:")
        if cho == 'a' or cho == 'A':
            # SQL连接测试
            connect_db_test()
        elif cho == 'b' or cho == 'B':
            # 同步下载Etherscan代码
            sync_mainnet_code()
            pass
        elif cho == 'c' or cho == 'C':
            # 根据id删除漏洞报告
            inreportid = input("Please Enter Report ID:")
            del_report_by_id(inreportid)
        elif cho == 'd' or cho == 'D':
            # 清空用户数据
            clean_data()
        elif cho == 'q' or cho == 'Q':
            break  # 返回上一菜单
        else:
            print("Input Error")


# 主菜单
def menu():
    _logo()
    while True:
        print("-----——--------Main-----——--------")
        print(" [a] Utility Toolbox")
        print(" [b] Vulnerability Detection")
        print(" [c] Result Query")
        print(" [d] Admin Panel")
        print(" [q] Exit")
        print("----------------------------------")
        choose = input("Please input choose:")
        if choose == 'a' or choose == 'A':
            # 实用工具箱
            toolbox()
        elif choose == 'b' or choose == 'B':
            # 漏洞检测模块
            vul_detection()
            pass
        elif choose == 'c' or choose == 'C':
            # 检测结果查询
            result_query()
            pass
        elif choose == 'd' or choose == 'D':
            # 管理面板
            admin_panel()
            pass
        elif choose == 'q' or choose == 'Q':
            sys.exit()  # 退出程序
        else:
            print("Input Error")
