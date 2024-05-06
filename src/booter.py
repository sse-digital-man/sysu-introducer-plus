from message import Message, MessageKind

from module.interface import BasicModule
from module.interface.info import ModuleStatus
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
        def crawler_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self.send(message)

        crawler_module: CrawlerInterface = self._sub_module("crawler")
        crawler_module.set_receive_callback(crawler_callback)

    # 单独运行和停止模块子模块
    def start_sub_module(self, name: str):
        self._load_config()
        self._sub_module(name).start()
        self._set_status(ModuleStatus.Running)

    def stop_sub_module(self, name: str):
        self._sub_module(name).stop()

    def send(self, message: Message):
        self._sub_module("core").send(message)

