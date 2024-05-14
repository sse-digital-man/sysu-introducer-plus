from message import Message, MessageKind

from .core import BasicCore, HandleResult
from .interface import ModuleName, BooterInterface
from .interface.info import ModuleStatus
from .crawler.interface import CrawlerInterface
from .renderer.interface import RendererInterface


class BasicBooter(BooterInterface):
    """数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
    1. 控制各个子部件的运行与停止
    2. 连接组件之间的交互

    """

    def __init__(self):
        super().__init__()

        self.__core: BasicCore = None

    def load_config(self):
        pass

    def before_starting_submodules(self):
        core: BasicCore = self._sub_module(ModuleName.CORE)
        self.__core = core

        # 1. 设置爬虫的接受回调函数
        crawler: CrawlerInterface = self._sub_module(ModuleName.CRAWLER)

        def receive_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            core.send(message)

        crawler.set_receive_callback(receive_callback)

        # 2. 设置 处理核心处理完成的回调函数
        renderer: RendererInterface = self._sub_module(ModuleName.RENDERER)

        def handle_callback(result: HandleResult):
            # TODO: 完善处理核心处理完成后的回调函数
            if renderer is None or renderer.status != ModuleStatus.Started:
                return  

            renderer.speak(result.sound_path)

        core.set_handle_callback(handle_callback)

    def send(self, msg: Message):
        self.__core.send(msg)
