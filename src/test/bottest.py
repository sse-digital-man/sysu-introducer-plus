import sys; sys.path.append("./src")
# from module.bot.ESbot import ESBot\
from module.bot import BasicBot
import csv, os

import openai
from module.interface.manager import manager
import time
manager.load_modules()

if __name__ == '__main__':
    bot = BasicBot()
    bot.start()
    # while True:
    #     user_input = input("----输入查询的内容:")
    #     start = time.perf_counter()
    #     res = bot.talk(user_input)
    #     end = time.perf_counter()
    #     print("----time:", end - start)
    #     print("----回答为:", res,"\n\n")


    file_path = "./data/test_messages.txt"
    output_path = "./data/test.csv"
    # 读取文本文件
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 创建 CSV 文件并写入表头
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['问题', '回答', '时间'])
        # 针对每一行进行操作
        for line in lines:
            start = time.perf_counter()
            try:
                res = bot.talk(line)
                end = time.perf_counter()
                # 将问题、回答和时间写入 CSV 文件
                writer.writerow([line, res, end - start])
                print("----回答的问题:", line)
                print("----time:", end - start)
                print("----回答为:", res, "\n\n")
            except openai.APITimeoutError: 
                print("timeout")
                pass
                