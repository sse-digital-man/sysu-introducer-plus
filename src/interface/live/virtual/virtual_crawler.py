from typing import List
from threading import Thread
import time

from utils.config import config
from ..crawler import CrawlerInterface

DEFAULT_DELAY = 1

def file_to_list(path: str) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines(-1)

class VirtualCrawler(CrawlerInterface):
    def __init__(self, receive_callback):
        super().__init__(receive_callback)

        # self.__message_list_path = "./data/test_message_list.txt"
        self.__messages = []
        self.__is_running = False
        self.__generate_thread = None
        self.__delay = DEFAULT_DELAY

    
    def start(self):
        self.load_config()

        self.__is_running = True
        self.__generate_thread = Thread(target=self.__generate_message)
        self.__generate_thread.start()
    
    def stop(self):
        self.__is_running = False
        self.__generate_thread.join()

    def load_config(self):
        info = config.get_system_interface("live", "virtual")

        self.__delay = info['delay'] / 1000
        self.__messages = file_to_list(info['messages_path'])
    
    def __generate_message(self):
        index = 0

        n = len(self.__messages)

        while(self.__is_running and n > 0):
            msg = self.__messages[index]
            self._receive_callback(msg)

            index = (index + 1) % n
            
            # 等待一段时间
            time.sleep(self.__delay)


        
        
    