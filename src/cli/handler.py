from typing import List
from tabulate import tabulate

from module.interface.info import moduleStatusMap, ModuleName
from core import BasicCore
from message import Message, MessageKind
from . import manager
from .kind import CommandHandleError, CommandUsageError

BOOTER = ModuleName.Booter.value

def handle_start(args: List[str]):
    length = len(args)
    # 如果运行没有参数，则运行所有参数
    if length == 1:
        manager.start(BOOTER)
    elif length == 2:
        module = args[1]
        manager.start(module)
    else:
        raise CommandUsageError(args[0])

# m
def handle_stop(args: List[str] = ["stop"]):
    length = len(args)

    if length == 1:
        manager.stop(BOOTER)
    elif length == 2:
        module = args[1]
        manager.stop(module)
    else:
        raise CommandUsageError(args[0])


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
                raise CommandHandleError(f"unknown field name '{header}'")
        
        rows.append(row)

    print()
    print(tabulate(rows, headers, tablefmt="github"))

def handle_exit(ignored): 
    manager.stop(BOOTER)
    raise InterruptedError()

def handle_change(args: List[str]):
    try:
        name, kind = args[1:]

        manager.change_module_kind(name, kind)
    except ValueError:
        raise CommandUsageError(args[0])

def handle_send(args: List[str]):
    try:
        if len(args) != 2:
            raise ValueError()
        message = Message(MessageKind.Admin, eval(args[1]))
    except:
        raise CommandUsageError(args[0])

    # 如果消息未能发送成功，则说明模块未启动
    if not manager.module(BOOTER).send(message):
        raise CommandHandleError("module is not running, can't send message")