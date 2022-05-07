from multiprocessing import Process

from mystery.analysis.myth_analyzer import run_myth
from mystery.analysis.slither_analyzer import run_slither
from mystery.utils import *


def run_analysis_tools(file_path, timeout):
    processes = []
    args = (os.path.abspath(file_path), timeout)
    processes.append(Process(target=run_myth, args=args))
    processes.append(Process(target=run_slither, args=args))

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    # FileName, ExtensionName = os.path.splitext(file_path)
    f_name = os.path.splitext(file_path)[0]
    # print(f_name)
    report_path = os.path.join(f_name + "_report.json")
    # print(report_path)
    # 保存检测告到.data目录下
    save_report_txt(file_path, report_path)



