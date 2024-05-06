from enum import Enum

from utils.args import args

from module.interface.manager import manager
from booter import BasicBooter

booter = BasicBooter()

class CommandKind(Enum):
    Start = "start"
    Stop = "stop"
    Status = "status"
    Exit = "exit"

def check_cmd(text: str) -> CommandKind:
    try:
        return CommandKind(text)
    except:
        return None

# 系统初始化操作
def init():
    # Notice: 需要再运行时统一加载完模块
    manager.load_modules()

def main():
    has_started = False
    # 初始化运行指令
    initial_command = [
        ["start", "core"], 
        ["status"]
    ]

    init()

    while True:
        try:
            # 初次自动运行
            if args.auto and not has_started:
                input_args = ["start"]
            # 是否运行初始化指令
            if args.init and len(initial_command) > 0:
                input_args = initial_command.pop(0)
            else:
                input_args = input("> ").split()

            cmd = check_cmd(input_args[0])

            if cmd == None:
                print("unknown command")
                continue

            if cmd is CommandKind.Start:
                length = len(input_args)
                # 如果运行没有参数，则运行所有参数
                if length == 1:
                    booter.start()
                else:
                    module = input_args[1]
                    booter.start_sub_module(module)
            elif cmd is CommandKind.Stop:
                booter.stop()
            elif cmd is CommandKind.Status:
                from tabulate import tabulate

                info_list = manager.module_info_list

                headers = ["name", "alias", "kind", "status"]
                rows = [
                    [
                        info[header] for header in headers
                    ] for info in info_list
                ]

                print()
                print(tabulate(rows, headers, tablefmt="github"))
            elif cmd is CommandKind.Exit:
                return
        except Exception as e:
            print("error:", repr(e))
            booter.stop()
            # raise e

if __name__ == '__main__':
    main()