from typing import Tuple

from message import Message, MessageKind

from module.interface.info import ModuleStatus
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
    
    def _before_starting(self):
        self.__set_receive_callback()

    # 单独运行和停止模块子模块
    def start_sub_module(self, name: str) -> Tuple[bool, ModuleStatus]:
        if name == "crawler":
            self.__set_receive_callback()

        return self._sub_module(name).start()

    def stop_sub_module(self, name: str) -> Tuple[bool, ModuleStatus]:
        # 验证当前是否只有最后一个启动
        return self._sub_module(name).stop()

    def send(self, message: Message) -> bool:
        return self._sub_module("core").send(message)

    def __set_receive_callback(self):
        def crawler_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self.send(message)

        crawler_module: CrawlerInterface = self._sub_module("crawler")
        crawler_module.set_receive_callback(crawler_callback)
