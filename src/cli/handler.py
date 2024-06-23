from typing import List
from tabulate import tabulate

from utils.error import ModuleLoadError

from framework.info import moduleStatusMap, ModuleName
from framework.manager import MANAGER
from framework.docker.client import DOCKER_CLIENT

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
        MANAGER.start(name)
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
    info_list = MANAGER.instance_list

    if len(info_list) == 0:
        print()
        print("not data")
        return

    # 输入显示的字段名
    keys = list(info_list[0].keys())
    if len(args) > 1:
        headers = args[1:]

        # 对输入的头部进行校验
        for header in headers:
            if header not in keys:
                raise CommandHandleError(f"unknown field name '{header}'")
    else:
        headers = keys

    # 将信息对象处理成行数据
    def gen_cell(info: dict, header: str):
        cell = info.get(header)

        if cell is None:
            cell = None
        elif header == "status":
            cell = moduleStatusMap[cell]
        elif header in ("kinds", "modules"):
            cell = ", ".join(cell)

        return cell

    rows = [[gen_cell(info, header) for header in headers] for info in info_list]

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


def handle_docker(args: List[str]):
    if len(args) < 4:
        raise CommandUsageError(args[0])

    [cmd, name, kind] = args[1:]

    if cmd not in ["start", "stop"]:
        raise CommandUsageError(args[0])

    if not DOCKER_CLIENT.check_instance_has_docker(name, kind):
        raise CommandHandleError(
            f"the kind '{kind}' of name '{name}' doesn't have docker"
        )

    if cmd == "start":
        DOCKER_CLIENT.start_module_container(name, kind)
    elif cmd == "stop":
        DOCKER_CLIENT.stop_module_container(name, kind)


def handle_reload(_ignored): ...
