from typing import List
from tabulate import tabulate

from module.interface.info import moduleStatusMap
from . import booter, manager

def handle_start(input_args: List[str]):
    length = len(input_args)
    # 如果运行没有参数，则运行所有参数
    if length == 1:
        booter.start()
    else:
        module = input_args[1]
        booter.start_sub_module(module)

def handle_stop(input_args: List[str]):
    booter.stop()

def handle_status(ignored):
    info_list = manager.module_info_list

    headers = ["name", "alias", "kind", "status"]

    # 将信息对象处理成行数据
    rows = []
    for info in info_list:
        row = []
        for header in headers:
            cell = info[header]
            if header == "status":
                row.append(moduleStatusMap[cell])
            else:
                row.append(cell)
        
        rows.append(row)

    print()
    print(tabulate(rows, headers, tablefmt="github"))

def handle_exit(ignored):
    booter.stop()
    raise InterruptedError()

def handle_change(input_args: List[str]):
    try:
        name, kind = input_args[1:]

        manager.change_module_kind(name, kind)
    except ValueError:
        print("usage: change name kind")