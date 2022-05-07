import os

from pyevmasm import assemble_hex


# Done
# Opcode to Bytecode
def opcode_to_bin(op_path):
    # print(op_path)
    if os.path.isfile(op_path):
        FileName, ExtensionName = os.path.splitext(op_path)
        if ExtensionName in ['.opcode']:
            with open(op_path, encoding="utf8") as op_file:
                opcode_inline = "\n".join(op_file.read().splitlines())
            bytecode_from_opcode = assemble_hex(opcode_inline)
            print("EVM Runtime ByteCode:\n" + bytecode_from_opcode[2:])
            with open(f"{FileName}-op.bin-runtime", "wb", buffering=0) as f:
                f.write(bytes(bytecode_from_opcode, encoding='utf8'))
                f.flush()
                os.fsync(f.fileno())
            print("Evm File Saved Success.")
        else:
            print("Invalid file.")
    elif os.path.isdir(op_path):
        # 读入文件夹
        files1 = os.listdir(op_path)
        # print(files1)
        # 统计一级文件夹中的二级文件夹个数
        num1 = len(files1)
        for i in range(num1):
            plist = os.path.splitext(files1[i])
            if plist[1] in ['.opcode']:
                print("------------------\nFilename: " + files1[i])
                signal_fpath = f"{op_path + '/' + files1[i]}"
                p_signal = os.path.splitext(signal_fpath)
                with open(signal_fpath, encoding="utf8") as op_file:
                    opcode_inline = "\n".join(op_file.read().splitlines())
                    bytecode_from_opcode = assemble_hex(opcode_inline)
                    print("EVM Runtime ByteCode:\n" + bytecode_from_opcode)
                    with open(f"{p_signal[0]}-op.bin-runtime", "wb", buffering=0) as f:
                        f.write(bytes(bytecode_from_opcode, encoding='utf8'))
                        f.flush()
                        os.fsync(f.fileno())
                    print("Evm File Saved Success.")
    else:
        print("Please enter a valid file or directory path.")
