import time
from typing import Callable

from message import MessageKind, Message
from module.interface.log import LOGGER, MessageLog
from module.interface import BasicModule

from .msg_queue.fifo_queue import FIFOQueue as MessageQueue


class HandleResult:
    def __init__(self, sound_path: str):
        self.sound_path = sound_path


HandleCallback = Callable[[HandleResult], None]


class BasicCore(BasicModule):
    def __init__(self):
        super().__init__()

        # 初始化消息队列
        self.__msg_queue = MessageQueue()

        self.__handle_callback: HandleCallback | None = None

    def load_config(self):
        pass

    def handle_starting(self):
        self._make_thread(self.__handle)

    # 线程循环处理消息队列（需要开启多线程）
    def __handle(self):

        # 当 Core 停止后，处理线程也需要停止
        while self._is_ready:
            time.sleep(0.5)
            if self.__msg_queue.empty():
                continue

            # 接收消息
            message = self.__msg_queue.pop()
            LOGGER.log(MessageLog.from_message(message))

            # 生成回答
            response = self._sub_module("bot").talk(message.content)
            LOGGER.log(
                MessageLog(
                    MessageKind.Assistant,
                    response,
                    # 如果是管理员发送的消息 则需要专门发给管理员
                    to_admin=message.kind == MessageKind.Admin,
                )
            )

            # 生成语音
            speech = self._sub_module("speaker").speak(response)

            # 响应处理结果, 只有对应回调函数非空时, 才进行处理
            if self.__handle_callback is not None:
                result = HandleResult(sound_path=speech)
                self.__handle_callback(result)

        # 核心处理完毕之后 清除消息队列
        self.__msg_queue.clear()

    def send(self, text: Message) -> bool:
        # 只有当处理核心运行时 才能向其添加消息
        if not self.is_running:
            return False

        self.__msg_queue.push(text)
        return True

    def set_handle_callback(self, callback: HandleCallback):
        self.__handle_callback = callback
