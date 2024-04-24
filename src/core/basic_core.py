from threading import Thread
import time

from message import Message
from core.msg_queue.fifo_queue import FIFOQueue as MessageQueue
from module.interface import ModuleInterface
from module.llm import Bot

class BasicCore(ModuleInterface):
    def __init__(self):
        super().__init__("core", "main")
    
        # 初始化消息队列
        self.__msg_queue = MessageQueue()
        self.__bot = Bot()

        self.__is_running = False
        self.__handle_thread = None

    def _load_config(self):
        pass

    def _load_sub_modules(self):
        self._add_sub_modules({
            "llm": Bot()
        })

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
        with super().start():
            self.__handle_thread = Thread(target=self.__handle)
            self.__handle_thread.start()

    def stop(self):
        with super().stop():
            # 关闭以上所有服务
            self.__handle_thread.join()

    def send(self, text: Message):
        self.__msg_queue.push(text)
    
    def check(self):
        return True