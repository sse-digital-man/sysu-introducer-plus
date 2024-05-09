from typing import List
from tabulate import tabulate

from module.interface.info import moduleStatusMap
from . import booter, manager

def handle_start(args: List[str]):
    length = len(args)
    # 如果运行没有参数，则运行所有参数
    if length == 1:
        booter.start()
    else:
        module = args[1]
        booter.start_sub_module(module)

def handle_stop(args: List[str]):
    if len(args) == 1:
        booter.stop()
    else:
        module = args[1]
        booter.stop_sub_module(module)

def handle_status(args: List[str]):
    info_list = manager.module_info_list

    # 输入显示的字段名
    headers = args[1:] if len(args) > 1 \
        else ["name", "alias", "kind", "kinds", "status"]

    # 将信息对象处理成行数据
    rows = []
    for info in info_list:
        row = []
        for header in headers:
            try:
                cell = info[header]
                if header == "status":
                    cell = moduleStatusMap[cell]
                if header == "kinds":
                    cell = ", ".join(cell)

                row.append(cell)
            
            except KeyError:
                raise KeyError(f"unknown field name '{header}'")
        
        rows.append(row)

    print()
    print(tabulate(rows, headers, tablefmt="github"))

def handle_exit(ignored): 
    booter.stop()
    raise InterruptedError()

def handle_change(args: List[str]):
    try:
        name, kind = args[1:]

        manager.change_module_kind(name, kind)
    except ValueError:
        print("usage: change name kind")