from typing import List
import time

from ...interface import VIRTUAL
from ..interface import CrawlerInterface

DEFAULT_DELAY = 1

def file_to_list(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        messages = f.readlines(-1)
        
        # 清除换行符
        for i in range(len(messages)):
            messages[i] = messages[i].strip()

        return messages

class VirtualCrawler(CrawlerInterface):
    def __init__(self):
        super().__init__()

        self.__messages = []
        self.__delay = DEFAULT_DELAY
        
    def _load_config(self):
        info = self._read_config()

        self.__delay = info['delay'] / 1000
        self.__messages = file_to_list(info['messages_path'])

        if len(self.__messages) == 0:
            print("[warning] messages is empty")

    def _after_running(self):
        self._make_thread(self.__generate_messages)

    def __generate_messages(self):
        index = 0

        n = len(self.__messages)

        while self.is_running and n > 0:
            msg = self.__messages[index]
            self._receive_callback(msg)

            index = (index + 1) % n
            
            # 等待一段时间
            time.sleep(self.__delay)