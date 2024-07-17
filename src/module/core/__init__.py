import time
from typing import Callable
from queue import LifoQueue
from message import MessageKind, Message
from module.interface import BasicModule
from module.queue.interface import QueueInterface
from module.bot.interface import BotInterface
from module.speaker.interface import SpeakerInterface
from framework.log import LOGGER, MessageLog


class HandleResult:
    def __init__(self, sound_path: str):
        self.sound_path = sound_path


HandleCallback = Callable[[HandleResult], None]


class BasicCore(BasicModule):
    def __init__(self):
        super().__init__()

        self.__handle_callback: HandleCallback | None = None
        self.__render_task_queue = LifoQueue(maxsize=1)

    def load_config(self):
        pass

    def handle_starting(self):
        self._make_thread(self.__handle)
        self._make_thread(self.__handle_render)

    def __handle_render(self):
        while self._is_ready:
            handle_result = self.__render_task_queue.get(block=True, timeout=None)
            if handle_result is None:
                continue

            self.__handle_callback(handle_result)

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
            response = self.__bot.talk(message.content)
            LOGGER.log(
                MessageLog(
                    MessageKind.Assistant,
                    response,
                    # 如果是管理员发送的消息 则需要专门发给管理员
                    to_admin=message.kind == MessageKind.Admin,
                )
            )

            # 生成语音
            speech = self.__speaker.speak(response)

            # 响应处理结果, 只有对应回调函数非空时, 才进行处理
            if self.__handle_callback is not None:
                result = HandleResult(sound_path=speech)
                self.__render_task_queue.put(result, block=True)
                # 添加空，主要是用于占位 (超时主要是防止上一条消息播放过久)
                self.__render_task_queue.put(None, block=True, timeout=30)

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

    @property
    def __msg_queue(self) -> QueueInterface:
        return self._sub_module("queue")
    
    @property
    def __bot(self) -> BotInterface:
        return self._sub_module("bot")

    @property
    def __speaker(self) -> SpeakerInterface:
        return self._sub_module("speaker")
