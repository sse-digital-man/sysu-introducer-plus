from core import BasicCore, HandleResult
from message import Message, MessageKind

from module.interface import BasicModule
from module.interface.info import ModuleName, ModuleStatus
from module.crawler.interface import CrawlerInterface
from module.renderer.interface import RendererInterface


class BasicBooter(BasicModule):
    """数字人 Core 的引导程序，用于封装包括 Core，Communicate，Interface 在内的多个组件，并提供以下操作：
    1. 控制各个子部件的运行与停止
    2. 连接组件之间的交互

    """
    def _load_config(self):
        pass

    def _before_starting_submodules(self):
        core: BasicCore = self._sub_module(ModuleName.Core)

        # 1. 设置爬虫的接受回调函数
        crawler: CrawlerInterface = self._sub_module(ModuleName.Crawler)

        def receive_callback(text: str):
            message = Message(MessageKind.Watcher, text)
            core.send(message)

        crawler.set_receive_callback(receive_callback)

        # 2. 设置 处理核心处理完成的回调函数
        renderer: RendererInterface = self._sub_module(ModuleName.Renderer)

        def handle_callback(result: HandleResult):
            # TODO: 完善处理核心处理完成后的回调函数
            if renderer is None or renderer.status != ModuleStatus.Starting:
                return

            renderer.speak(result.sound_path)

        core.set_handle_callback(handle_callback)
