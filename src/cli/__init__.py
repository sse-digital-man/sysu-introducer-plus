import sys
from typing import List
from importlib import import_module

from utils.error import ModuleError
from .args import args
from .kind import check_cmd, CommandHandleError, UnknownCommandError
from .handler import handle_stop


def print_error(e: Exception):
    print(type(e).__name__, ":", e.args[0])


class CliApp:
    def __init__(self, init_cmd: List[List[str]] = None):
        self.__has_started = False
        self.__init_cmd = [] if init_cmd is None else init_cmd

    def __get_input_args(self) -> List[str]:
        # 初次自动运行
        if args.auto and not self.__has_started:
            input_args = ["start"]
        # 是否运行初始化指令
        if args.init and len(self.__init_cmd) > 0:
            input_args = self.__init_cmd.pop(0).split()
        else:
            input_args = input("> ").split()

        return input_args

    def handle(self):
        while True:
            try:
                # 1. 读取输入参数
                input_args = self.__get_input_args()

                # 2. 验证指令非空，且存在
                if len(input_args) == 0:
                    continue
                cmd = input_args[0]
                if not check_cmd(cmd):
                    raise UnknownCommandError()

                # 3. 动态导入并调用处理函数
                handle_function = getattr(import_module("cli.handler"), f"handle_{cmd}")

                handle_function(input_args)

            # 当出现指令处理错误时 只需要打印即可
            except (CommandHandleError, ModuleError) as e:
                print_error(e)
            except InterruptedError:
                # 退出程序时 应该先停止该程序
                handle_stop(["stop"])
                sys.exit()
            except Exception as e:
                if args.force:
                    raise e
                print_error(e)
