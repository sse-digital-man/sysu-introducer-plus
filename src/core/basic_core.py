from threading import Thread
import time

from message import Message
from core.msg_queue.fifo_queue import FIFOQueue as MessageQueue

class BasicCore:
    def __init__(self):
        # 初始化消息队列
        self.__msg_queue = MessageQueue()

        self.__handle_thread = Thread(target=self.__handle)
        
    
    # 线程循环处理消息队列（需要开启多线程）
    def __handle(self):
        # ...
        while True:
            time.sleep(0.5)

            if self.__msg_queue.empty():
                continue

            message = self.__msg_queue.pop()

            # 处理逻辑
            print("receive:", message.content)

    def start(self):
        print("数字人内核启动")

        self.__handle_thread.start()

        # 验证 LLM 是否正常

        # 检测 TTS 是否正常

        # 检测 View 是否正常
        pass

    def stop(self):
        # 关闭以上所有服务
        pass

    def send(self, text: Message):
        self.__msg_queue.push(text)
    
    def update_config(self):
        # 直播间、房间号配置
        pass