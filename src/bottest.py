from module.llm.bot.gpt import GPTBot
import time
if __name__ == '__main__':
    bot = GPTBot()
    while True:
        user_input = input("----输入查询的内容:")
        start = time.perf_counter()
        res = bot.talk(user_input)
        end = time.perf_counter()
        print("----time:", end-start)
        print("----回答为:", res,"\n\n")