from typing import List
from tabulate import tabulate

from utils.error import ModuleLoadError

from module.interface.info import moduleStatusMap, ModuleName
from module.interface.manager import MANAGER
from message import Message, MessageKind
from .kind import CommandHandleError, CommandUsageError

BOOTER = ModuleName.BOOTER.value


def handle_start(args: List[str]):
    length = len(args)
    # 如果运行没有参数，则运行所有参数
    if length in (1, 2):
        name = BOOTER
        if length == 2:
            name = args[1]
        MANAGER.start(name, with_sub=True, with_sup=True)
    else:
        raise CommandUsageError(args[0])


def handle_stop(args: List[str]):
    length = len(args)

    if length in (1, 2):
        name = BOOTER
        if length == 2:
            name = args[1]
        MANAGER.stop(name)
    else:
        raise CommandUsageError(args[0])


def handle_status(args: List[str]):
    info_list = MANAGER.module_list

    # 输入显示的字段名
    headers = (
        args[1:] if len(args) > 1 else ["name", "alias", "kind", "kinds", "status"]
    )

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


def handle_exit(_ignored):
    MANAGER.stop(BOOTER)
    raise InterruptedError()


def handle_change(args: List[str]):
    try:
        name, kind = args[1:]

        MANAGER.change_module_kind(name, kind)
    except ModuleLoadError as e:
        raise e
    except ValueError:
        raise CommandUsageError(args[0])


def handle_send(args: List[str]):
    try:
        if len(args) != 2:
            raise ValueError()
        message = Message(MessageKind.Admin, eval(args[1]))
    except BaseException:
        raise CommandUsageError(args[0])

    # 如果消息未能发送成功，则说明模块未启动
    MANAGER.send(message)


def handle_reload(_ignored): ...
