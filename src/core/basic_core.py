from threading import Thread
import time

from message import Message
from core.msg_queue.fifo_queue import FIFOQueue as MessageQueue
from module.llm.bot import Bot

class BasicCore:
    def __init__(self):
        # 初始化消息队列
        self.__msg_queue = MessageQueue()
        self.__bot: Bot = Bot()

        self.__is_running = False
        self.__handle_thread = None

    
    # 线程循环处理消息队列（需要开启多线程）
    def __handle(self):
        # ...
        while True:
            time.sleep(0.5)

            # 当 Core 停止后，处理线程也需要停止
            if not self.__is_running:
                self.__msg_queue.clear()
                break

            if self.__msg_queue.empty():
                continue

            message = self.__msg_queue.pop()
            print("receive:", message.content)

            response = self.__bot.talk(message.content)
            print("answer:", response)

        

    def start(self):
        print("数字人内核启动")

        # 验证 LLM 是否正常
        flag, error = self.__bot.check()
        if not flag:
            raise RuntimeError("LLM 模块监测失败：" + repr(error))
                
        self.__handle_thread = Thread(target=self.__handle)
        self.__handle_thread.start()


        # 检测 TTS 是否正常

        # 检测 View 是否正常

        self.__is_running = True

    def stop(self):
        self.__is_running = False
        # 关闭以上所有服务
        self.__handle_thread.join()

    def send(self, text: Message):
        self.__msg_queue.push(text)
    
    def update_config(self):
        # 直播间、房间号配置
        pass