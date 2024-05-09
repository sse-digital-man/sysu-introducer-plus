import sys; sys.path.append("./src")
from importlib import import_module

from cli.args import args
from cli.kind import check_cmd, UnknownCommandError
from cli import booter

def print_error(e: Exception):
    print(type(e).__name__, ":", e.args[0])


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
                raise UnknownCommandError()

            handle_function = \
                import_module("cli.handler").__getattribute__(f"handle_{cmd.value}")

            handle_function(input_args)

        # 未知指令不需要特殊处理
        except UnknownCommandError as e:
            print_error(e)
        except InterruptedError:
            exit()
        except Exception as e:
            if not args.force:
                print_error(e)
            else:
                raise e
            booter.stop()

if __name__ == '__main__':
    main()