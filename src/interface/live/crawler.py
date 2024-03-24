from abc import ABCMeta, abstractmethod


class CrawlerInterface(metaclass=ABCMeta):
    room_id = 407149

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