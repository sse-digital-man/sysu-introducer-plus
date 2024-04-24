from typing import Dict

from core.basic_core import BasicCore as Core
from message import Message, MessageKind

from module.interface import ModuleInterface
from module.live import LiveCrawler, CrawlerInterface
from module.llm import Bot

'''
数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
1. 控制各个子部件的运行与停止
2. 连接组件之间的交互
'''
class Booter(ModuleInterface):
    def __init__(self):
        super().__init__("booter", "main")

    def _load_config(self):
        pass

    def _load_sub_modules(self):
        def crawler_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self.send(message)

        self._add_sub_modules({
            "live": LiveCrawler(crawler_callback),
            "core": Core(),
        })
    
    def check(self) -> bool:
        return True

    def send(self, message: Message):
        self.__core.send(message)