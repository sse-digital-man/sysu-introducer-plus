from abc import ABCMeta, abstractmethod

from utils.config import config


class CrawlerInterface(metaclass=ABCMeta):
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

    @property
    def _room_id(self) -> int:
        """这里需要使用动态加载的方式，读取房间号

        Returns:
            int: 房间号
        """
        return config.get_system_interface("live", "bilibili", "roomId")