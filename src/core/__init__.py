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

        # 当 Core 停止后，处理线程也需要停止
        while self._is_ready:
            time.sleep(0.5)
            if self.__msg_queue.empty():
                continue
            
            message = self.__msg_queue.pop()
            print("receive:", message.content)

            response = self._sub_module("bot").talk(message.content)
            print("answer:", response)

        # 核心处理完毕之后 清除消息队列
        self.__msg_queue.clear()

    def _before_started(self):
        self._make_thread(self.__handle)

    def send(self, text: Message) -> bool:
        # 只有当处理核心运行时 才能向其添加消息
        if self.is_running:
            self.__msg_queue.push(text)
            return True

        return False