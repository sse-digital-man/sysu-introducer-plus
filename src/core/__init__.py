import time

from message import Message
from core.msg_queue.fifo_queue import FIFOQueue as MessageQueue

from module.interface import ModuleInterface

class BasicCore(ModuleInterface):
    def __init__(self):
        super().__init__("core")
    
        # 初始化消息队列
        self.__msg_queue = MessageQueue()

        self._set_startup_func(self.__handle)
        self._set_sub_modules(["bot"])
    def _load_config(self):
        pass

    # 线程循环处理消息队列（需要开启多线程）
    def __handle(self):
        # ...
        while True:
            time.sleep(0.5)

            # 当 Core 停止后，处理线程也需要停止
            if not self.is_running:
                self.__msg_queue.clear()
                break

            if self.__msg_queue.empty():
                continue

            message = self.__msg_queue.pop()
            print("receive:", message.content)

            response = self.__bot.talk(message.content)
            print("answer:", response)

    def send(self, text: Message):
        self.__msg_queue.push(text)
    
    def check(self):
        return True