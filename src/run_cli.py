import sys
from cli import CliApp

sys.path.append("src")


def main():
    # 初始化运行指令
    initial_command = []

    app = CliApp(initial_command)
    app.handle()


if __name__ == "__main__":
    main()
