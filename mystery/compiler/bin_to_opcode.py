# Bytecode to Opcode
import os
import random
import string
from pyevmasm import disassemble_hex


# Done

def evm_to_opcode(byte_path):
    FileName, ExtensionName = os.path.splitext(byte_path)
    if os.path.isfile(byte_path):
        # 直接编译单独的*.bin-runtime文件
        if ExtensionName in ['.bin', '.bin-runtime']:
            with open(byte_path, encoding="utf8") as bytecode_file:
                byte_code = bytecode_file.read()
                if byte_code[:10] == '0x60806040' or byte_code[:8] == '60806040':
                    opcode_from_bytecode = disassemble_hex(byte_code)
                    with open(f"{FileName}-bin.opcode", "wb", buffering=0) as f:
                        f.write(bytes(opcode_from_bytecode, encoding='utf8'))
                        f.flush()
                        os.fsync(f.fileno())
                    print("Opcodes Saved Success.")
                else:
                    print("Invalid *.bin-runtime File.")
        else:
            print("Please Enter a valid file.")
    elif os.path.isdir(byte_path):
        # 读入文件夹
        files1 = os.listdir(byte_path)
        # print(files1)
        # 统计一级文件夹中的二级文件夹个数
        num1 = len(files1)
        for i in range(num1):
            plist = os.path.splitext(files1[i])
            if plist[1] in ['.bin', '.bin-runtime']:
                print("Filename: " + files1[i])
                signal_fpath = f"{byte_path + '/' + files1[i]}"
                p_signal = os.path.splitext(signal_fpath)
                with open(signal_fpath, encoding="utf8") as bytecode_file:
                    byte_code = bytecode_file.read()
                    if byte_code[:10] == '0x60806040' or byte_code[:8] == '60806040':
                        opcode_from_bytecode = disassemble_hex(byte_code)
                        with open(f"{p_signal[0]}-bin.opcode", "wb", buffering=0) as f:
                            f.write(bytes(opcode_from_bytecode, encoding='utf8'))
                            f.flush()
                            os.fsync(f.fileno())
                        print("Opcodes Saved Success.")
                    else:
                        print("Invalid *.evm File.")
    elif byte_path[:10] == '0x60806040' or byte_path[:8] == '60806040':
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        opcode_from_bytecode = disassemble_hex(byte_path)
        with open(f"{os.getcwd() + '/data/evm/' + ran_str}-bin.opcode", "wb", buffering=0) as f:
            f.write(bytes(opcode_from_bytecode, encoding='utf8'))
            f.flush()
            os.fsync(f.fileno())
        print("Opcodes Saved Success.")
    else:
        print("Please enter a valid file or directory path or bytecode.")
