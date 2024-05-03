from collections.abc import Callable

from ..interface import BasicModule

CRAWLER = "crawler"

CrawlerCallback = Callable[[str], None]

class CrawlerInterface(BasicModule):
    def __init__(self):
        """
        Args:
            name(str): 模块具体的实现方式
            receive_callback (function): 接收到消息的回调函数
        """
        super().__init__(CRAWLER)
        self._receive_callback = None

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
    
    ''' ----- Setter ----- '''
    def set_receive_callback(self, receive_callback: CrawlerCallback):
        self._receive_callback = receive_callback