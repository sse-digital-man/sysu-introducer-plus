import sys; sys.path.append("./src")
from typing import List
from importlib import import_module

from cli.args import args
from cli.kind import check_cmd, UnknownCommandError
from cli.handler import handle_stop

def print_error(e: Exception):
    print(type(e).__name__, ":", e.args[0])

class CliApp:
    def __init__(self, init_cmd: List[List[str]]=[]):
        self.__has_started = False
        self.__init_cmd = init_cmd

    def __get_input_args(self) -> List[str]:
        # 初次自动运行
        if args.auto and not self.__has_started:
            input_args = ["start"]
        # 是否运行初始化指令
        if args.init and len(self.__initial_command) > 0:
            input_args = self.__init_cmd.pop(0)
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
                cmd = check_cmd(input_args[0])
                if cmd == None:
                    raise UnknownCommandError()

                # 3. 动态导入并调用处理函数
                handle_function = \
                    import_module("cli.handler").__getattribute__(f"handle_{cmd.value}")

                handle_function(input_args)

            # 未知指令不需要特殊处理
            except UnknownCommandError as e:
                print_error(e)
            except InterruptedError:
                # 退出程序时 应该先停止该程序
                handle_stop()
                exit()
            except Exception as e:
                if  args.force:
                    raise e
                print_error(e)


def main():
    # 初始化运行指令
    initial_command = [
        ["start", "core"], 
        ["status"]
    ]

    app = CliApp(initial_command)
    app.handle()
                
if __name__ == '__main__':
    main()