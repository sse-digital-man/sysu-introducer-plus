from abc import ABCMeta, abstractmethod

from utils.config import LiveConfig


class CrawlerInterface(metaclass=ABCMeta):
    room_id = LiveConfig.ROOM_ID

    def __init__(self, receive_callback):
        """

        Args:
            receive_callback (function): 接收到消息的回调函数
        """
        self.receive_callback = receive_callback
    
    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...