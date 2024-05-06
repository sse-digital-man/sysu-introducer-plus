import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--auto", action="store_true", help="start after running")
parser.add_argument("--init", action="store_true", help="execute initial operation")

# 解析出来的参数
args = parser.parse_args()