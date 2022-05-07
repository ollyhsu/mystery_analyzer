# 从report_dir 中删除指定的report
import os
import sys

root_dir = os.getcwd()  # /home/hohin/mystery
# root_dir = "/home/hohin/mystery"
report_dir = os.path.join(root_dir, ".data/report/")


# 从report_dir 中获取report id list

def get_report_id_list():
    report_id_list = []
    # 从report_dir目录下遍历所有文件，并将文件名添加到report_id_list中
    for file in os.listdir(report_dir):
        filename = file.split(".")[0]
        fileid = filename.split("_")[0]
        report_id_list.append(fileid)
    return report_id_list


# 若report_id_list中不包含指定的report_id，则删除文件;否则，提示report_id不存在
def del_report_by_id(report_id):
    report_id_list = get_report_id_list()
    if report_id in report_id_list:
        # 循环遍历report_dir目录下的所有文件，找到report_id开头对应的文件
        for root, dirs, files in os.walk(report_dir):
            for file in files:
                if file.startswith(report_id):
                    # print(root + file)
                    os.remove(os.path.join(root, file))
                    sys.stdout.flush()
                    print("report_id: %s deleted." % report_id)
    else:
        print("report_id: %s not exist." % report_id)
