"""
清空 .data 文件夹下的所有文件
"""
import os
import sys


def clean_data():
    try:
        # 确认是否继续清理
        choice = input("Are you sure to clean all data? [y/n]")
        if choice == 'y' or choice == 'Y':
            # 获取项目工作空间
            work_space = os.getcwd()
            # work_space = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            # print(work_space)
            # 获取 .data 文件夹的路径
            data_path = os.path.join(work_space, '.data')
            # 清空.data文件夹下所有的普通文件，保留目录结构
            for root, dirs, files in os.walk(data_path):
                for file in files:
                    os.remove(os.path.join(root, file))
            sys.stdout.flush()  # 刷新缓冲区
            # 输出清空完成的提示信息
            print('Data has been cleaned!')
        else:
            print('Cancelled!')

    except Exception as e:
        print(e)
