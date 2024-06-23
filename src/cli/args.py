import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--auto", action="store_true", help="start after running")
# 该指令支持输入多个命令，按照空格划分
parser.add_argument("--init", nargs="+", help="execute initial operation")
parser.add_argument(
    "--force", action="store_true", help="program will interrupt when meet error"
)

# 解析出来的参数
args = parser.parse_args()
