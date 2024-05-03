from typing import Dict

from message import Message, MessageKind

from module.interface import BasicModule
from module.crawler import CrawlerInterface

'''
数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
1. 控制各个子部件的运行与停止
2. 连接组件之间的交互
'''
class BasicBooter(BasicModule):
    def __init__(self):
        super().__init__("booter")
        
    def _load_config(self):
        pass

    def _after_load_sub_modules(self):
        def crawler_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self.send(message)

        crawler_module: CrawlerInterface = self._module("crawler")
        crawler_module.set_receive_callback(crawler_callback)

    def send(self, message: Message):
        self._sub_modules["core"].send(message)

