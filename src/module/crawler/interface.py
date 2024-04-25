from collections.abc import Callable
from typing import NewType

from ..interface import ModuleInterface


from utils.config import config


CRAWLER = "crawler"

CrawlerCallback = Callable[[str], None]

class CrawlerInterface(ModuleInterface):
    def __init__(self, name: str, receive_callback: CrawlerCallback):
        """
        Args:
            name(str): 模块具体的实现方式
            receive_callback (function): 接收到消息的回调函数
        """
        super().__init__(CRAWLER, name)
        self._receive_callback = receive_callback

    def _load_config(self):
        info = self._read_config()
        
        self._room_id = info["roomId"]

    @property
    def _room_id(self) -> int:
        """这里需要使用动态加载的方式，读取房间号

        Returns:
            int: 房间号
        """
        return self._room_id