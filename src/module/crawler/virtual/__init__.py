import time

from utils.file import load_lines
from ..interface import CrawlerInterface

DEFAULT_DELAY = 1


class VirtualCrawler(CrawlerInterface):
    def __init__(self):
        super().__init__()

        self.__messages = []
        self.__delay = DEFAULT_DELAY

    def load_config(self):
        info = self._read_config()

        self.__delay = info["delay"] / 1000
        self.__messages = load_lines(info["messages_path"])

        if len(self.__messages) == 0:
            print("[warning] messages is empty")

    def handle_starting(self):
        self._make_thread(self.__generate_messages)

    def __generate_messages(self):
        index = 0

        n = len(self.__messages)

        while self._is_ready and n > 0:

            msg = self.__messages[index]
            self._receive_callback(msg)

            index = (index + 1) % n

            # 等待一段时间
            time.sleep(self.__delay)
