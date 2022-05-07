import os

root_dir = os.getcwd()  # /home/hohin/mystery
# root_dir = "/home/hohin/mystery"
report_dir = os.path.join(root_dir, ".data/report/")
# sol_fpath = "/home/hohin/mystery/.data/etherscan/code/0x45b3c08fbd84b8f9b26e3b5d27e158258628d2f5-ElitesCAW.sol"


def gen_new_id():
    id_list = []
    # 从report_dir目录下遍历所有文件，并将文件名添加到id_list中
    for file in os.listdir(report_dir):
        filename = file.split(".")[0]
        fileid = filename.split("_")[0]
        id_list.append(fileid)
    if not id_list:
        new_id = "1001"
    else:
        new_id = int(max(id_list)) + 1
    return new_id


def get_add_list():
    add_list = []
    for file in os.listdir(report_dir):
        filename = file.split(".")[0]
        filename = filename.split("_")[1]
        address = filename.split("-")[0]
        add_list.append(address)
    return add_list


# 检测report_dir是否存在address的报告文件，若存在则跳过，若不存在则生成新的报告文件
def check_report_file(address):
    alist = get_add_list()
    if address in alist:
        return True
    else:
        return False


def gen_report_file(sol_path, report_content):
    # 获取新的id
    new_id = gen_new_id()
    FileName, ExtensionName = os.path.splitext(sol_path)
    real_fname = FileName.split("/")[-1]
    add_name = real_fname.split("-")[0]
    alist = get_add_list()
    if add_name in alist:
        print(f"{add_name} already exists, skip.")
    else:
        # 生成新的报告文件
        report_file = os.path.join(report_dir, f"{new_id}_{real_fname}.txt")
        with open(report_file, "w") as f:
            f.write(report_content)
            f.flush()
            os.fsync(f.fileno())
        # 请牢记你的新报告文件的id
        print(f"Your VUL Report ID is: {new_id}")
        print(f"{new_id}_{real_fname} report file generated.")


# gen_report_file(sol_fpath, report_txt)
# # check_add_file()
