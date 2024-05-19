from message import Message, MessageKind

from .core import BasicCore, HandleResult
from .interface import BooterInterface
from .interface.info import ModuleStatus, ModuleName
from .crawler.interface import CrawlerInterface
from .renderer.interface import RendererInterface


class BasicBooter(BooterInterface):
    """数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
    1. 控制各个子部件的运行与停止
    2. 连接组件之间的交互

    """

    def load_config(self):
        pass

    def before_starting_submodules(self):
        # 1. 设置爬虫的接受回调函数
        def receive_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            self._core.send(message)

        self._crawler.set_receive_callback(receive_callback)

        # 2. 设置 处理核心处理完成的回调函数
        def handle_callback(result: HandleResult):
            # TODO: 完善处理核心处理完成后的回调函数
            if self._renderer is None or self._renderer.status != ModuleStatus.Started:
                return

            self._renderer.speak(result.sound_path)

        self._core.set_handle_callback(handle_callback)

    def send(self, msg: Message):
        self._core.send(msg)

    @property
    def _core(self) -> BasicCore:
        return self._sub_module(ModuleName.CORE)

    @property
    def _crawler(self) -> CrawlerInterface:
        return self._sub_module(ModuleName.CRAWLER)

    @property
    def _renderer(self) -> RendererInterface:
        return self._sub_module(ModuleName.RENDERER)
