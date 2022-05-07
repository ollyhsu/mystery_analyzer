import os
from pyevmasm import disassemble_hex
from mystery.compiler import get_sol_bytecode


# Done
# *.sol to Opcode
def sol_to_opcode(sol_path):
    s_list = os.path.splitext(sol_path)
    if os.path.isfile(sol_path):
        # 直接编译单独的sol文件
        b_code = str(get_sol_bytecode(sol_path))
        # print(b_code)
        if b_code[:10] == '0x60806040' or b_code[:8] == '60806040':
            opcode_from_bytecode = disassemble_hex(b_code)
            with open(f"{s_list[0]}-sol.opcode", "wb", buffering=0) as f:
                f.write(bytes(str(opcode_from_bytecode), encoding='utf8'))
                f.flush()
                os.fsync(f.fileno())
            print("Opcodes Saved Success.")
    elif os.path.isdir(sol_path):
        # 读入文件夹
        f1 = os.listdir(sol_path)
        # 统计一级文件夹中的二级文件夹个数
        num1 = len(f1)
        for i in range(num1):
            f_list = os.path.splitext(f1[i])
            if f_list[1] in ['.sol']:
                print("Filename: " + f1[i])
                signal_fpath = sol_path + '//' + f1[i]
                FileName, ExtensionName = os.path.splitext(signal_fpath)
                b_code = str(get_sol_bytecode(signal_fpath))
                # print(code)
                if b_code[:10] == '0x60806040' or b_code[:8] == '60806040':
                    opcode_from_bytecode = disassemble_hex(b_code)
                    with open(f"{FileName}-sol.opcode", "wb", buffering=0) as f:
                        f.write(bytes(str(opcode_from_bytecode), encoding='utf8'))
                        f.flush()
                        os.fsync(f.fileno())
                    print("Opcodes Saved Success.")
    else:
        print("Please enter a valid file or directory path.")
