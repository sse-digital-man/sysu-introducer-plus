from enum import Enum

from utils.args import args
from module.interface.manager import manager
from booter import BasicBooter

booter = BasicBooter()

class CommandKind(Enum):
    Start = "start"
    Stop = "stop"
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
    first_start_flag = False
    init()

    while True:
        try:
            # 设置启动程序后的自动运行
            if not first_start_flag and args.auto:
                cmd = CommandKind.Start
                first_start_flag = True
            else:
                cmd = check_cmd(input("> "))

            if cmd == None:
                print("unknown command")
                continue

            if cmd is CommandKind.Start:
                booter.start()
            elif cmd is CommandKind.Stop:
                booter.stop()
            elif cmd is CommandKind.Exit:
                return
        except Exception as e:
            print("error:", repr(e))
            raise e
        finally:
            booter.stop()

if __name__ == '__main__':
    main()