import sys

from utils import error
from .manager import ModuleManager


# Notice: 使用单例模式使用模块管理器
def init_manager() -> ModuleManager:
    try:
        manager = ModuleManager()
        manager.load()
    except error.ModuleLoadError as e:
        # 首次加载模块失败则会停止
        print(e.args[0])
        sys.exit()

    return manager


MANAGER = init_manager()
