import sys; sys.path.append("./src")
from importlib import import_module

from utils.args import args
from cli.kind import check_cmd
from cli import booter


def main():
    has_started = False
    # 初始化运行指令
    initial_command = [
        ["start", "core"], 
        ["status"]
    ]

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

            handle_function = \
                import_module("cli.handler").__getattribute__(f"handle_{cmd.value}")

            handle_function(input_args)
        except InterruptedError:
            exit()
        except Exception as e:
            print("error:", repr(e))
            booter.stop()
            # raise e

if __name__ == '__main__':
    main()