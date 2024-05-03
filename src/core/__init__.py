import time

from message import Message
from core.msg_queue.fifo_queue import FIFOQueue as MessageQueue

from module.interface import BasicModule

class BasicCore(BasicModule):
    def __init__(self):
        super().__init__("core")
    
        # 初始化消息队列
        self.__msg_queue = MessageQueue()
        
    def _load_config(self):
        pass

    # 线程循环处理消息队列（需要开启多线程）
    def __handle(self):
        # ...
        while self.is_running:
            time.sleep(0.5)
            # print("handling...")

            # 当 Core 停止后，处理线程也需要停止
            if not self.is_running:
                self.__msg_queue.clear()
                break

            if self.__msg_queue.empty():
                continue
            
            message = self.__msg_queue.pop()
            print("receive:", message.content)

            response = self._sub_module("bot").talk(message.content)
            print("answer:", response)

    def _after_running(self):
        self._make_thread(self.__handle)

    def send(self, text: Message):
        self.__msg_queue.push(text)