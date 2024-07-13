from message import Message, MessageKind

from framework.info import ModuleStatus, ModuleName
from framework import RootInterface

from .interface import BasicModule
from .core import BasicCore, HandleResult
from .crawler.interface import CrawlerInterface
from .renderer.interface import RendererInterface


class BasicBooter(RootInterface):
    """数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
    1. 控制各个子部件的运行与停止
    2. 连接组件之间的交互

    """

    def load_config(self):
        pass

    # 接收回调函数
    def __receive_callback(self, text: str):
        message = Message(MessageKind.Watcher, text)
        self._core.send(message)

    def __handle_callback(self, result: HandleResult):
        # TODO: 完善处理核心处理完成后的回调函数
        if self._renderer is None or self._renderer.status != ModuleStatus.Started:
            return

        self._renderer.speak(result.sound_path)

    def handle_starting(self):
        self._crawler.set_receive_callback(self.__receive_callback)
        self._core.set_handle_callback(self.__handle_callback)

    def send(self, msg: Message):
        self._core.send(msg)

    def update_submodule(self, name: str, sub_module: BasicModule):
        super().update_submodule(name, sub_module)

        if name == ModuleName.CRAWLER:
            self._crawler.set_receive_callback(self.__receive_callback)
        elif name == ModuleName.CORE:
            self._core.set_handle_callback(self.__handle_callback)

    @property
    def _core(self) -> BasicCore:
        return self._sub_module(ModuleName.CORE)

    @property
    def _crawler(self) -> CrawlerInterface:
        return self._sub_module(ModuleName.CRAWLER)

    @property
    def _renderer(self) -> RendererInterface:
        return self._sub_module(ModuleName.RENDERER)
