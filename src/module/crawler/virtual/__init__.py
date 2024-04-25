from typing import List
import time

from ...interface import VIRTUAL
from ..interface import CrawlerInterface, CrawlerCallback

DEFAULT_DELAY = 1

def file_to_list(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines(-1)

class VirtualCrawler(CrawlerInterface):
    def __init__(self):
        super().__init__(VIRTUAL)

        self.__messages = []
        self.__delay = DEFAULT_DELAY
        
        self._set_startup_func(self.__generate_message)

    def _load_config(self):
        info = self._read_config()

        self.__delay = info['delay'] / 1000
        self.__messages = file_to_list(info['messages_path'])

    def check(self) -> bool:
        return True

    def __generate_message(self):
        index = 0

        n = len(self.__messages)

        while(self.is_running and n > 0):
            msg = self.__messages[index]
            self._receive_callback(msg)

            index = (index + 1) % n
            
            # 等待一段时间
            time.sleep(self.__delay)


        
        
    