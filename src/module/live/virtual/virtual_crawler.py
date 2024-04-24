from typing import List
from threading import Thread
import time

from utils.config import config
from ..interface import CrawlerInterface, CrawlerCallback

DEFAULT_DELAY = 1

VIRTUAL = "virtual"

def file_to_list(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines(-1)

class VirtualCrawler(CrawlerInterface):
    def __init__(self, receive_callback: CrawlerCallback):
        super().__init__(VIRTUAL, receive_callback)

        # self.__message_list_path = "./data/test_message_list.txt"
        self.__messages = []
        self.__generate_thread = None
        self.__delay = DEFAULT_DELAY

    def _load_config(self):
        info = self._read_config()

        self.__delay = info['delay'] / 1000
        self.__messages = file_to_list(info['messages_path'])


    def start(self):
        with super().start():
            self.__generate_thread = Thread(target=self.__generate_message)
            self.__generate_thread.start()
    
    def stop(self):
        with super().stop():
            self.__generate_thread.join()

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


        
        
    