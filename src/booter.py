from core.basic_core import BasicCore as Core
from message import Message, MessageKind
from interface.live import LiveCrawler
from interface.live.crawler import CrawlerInterface




'''
数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
1. 控制各个子部件的运行与停止
2. 连接组件之间的交互
'''
class Booter:
    def __init__(self):
        def __live_crawler_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self.send(message)

        self.__live_crawler: CrawlerInterface = LiveCrawler(__live_crawler_callback)
        self.__core = Core()


    def start(self):
        self.__core.start()
        self.__live_crawler.start()


    def stop(self):
        self.__live_crawler.stop()
    
    def send(self, message: Message):
        self.__core.send(message)