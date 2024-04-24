from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import Dict, Self

from utils.config import config

class ModuleInterface(metaclass=ABCMeta):
    def __init__(self, kind: str, name: str):
        """ 初始化函数

        Args:
            kind (str): 模块类型
            name (str): 模块具体的名称
        """
        self.__is_running = False
        self.__kind = kind
        self.__name = name

        self.__sub_modules: Dict[str, ModuleInterface] = {}

    # 该函数主要由模块管理器统一进行管理，统一进行更新
    @abstractmethod
    def _load_config(self):
        # 需要每次更新配置文件以保证最新
        pass

    # 封装加载何种子模块
    def _load_sub_modules(self):
        pass

    # 如果验证成功则直接通过，失败则 raise 错误
    # 主要是用于是否能够正常启动模块
    @abstractmethod
    def check(self) -> bool:
        ...

    # 启动模块单元
    @contextmanager
    def start(self):
        # 更新
        self._load_config()
        self._load_sub_modules()

        # 循环启动各个子模块
        for module in self.__sub_modules.values():
            if not module.check():
                print(module.name, "check error")
                return
            module.start()

        # 上下文控制器 https://zhuanlan.zhihu.com/p/317360115
        # yield None
        yield None

        # TODO:
        print(self.kind_with_name + ": start successfully")

        # Notice: 只有所有程序启动成功之后 才能更新状态
        self.__is_running = True

    # 停止模块单元
    def stop(self):
        try:
            for module in self.__modules.values():
                module.stop()
        except Exception:
            pass
        finally:
            # 无论如何 最后都需要更新状态
            self.__is_running = False

    # 添加子模块
    def _add_sub_modules(self, modules: Dict[str, Self]):
        # Notice: 模块启动时也会按照如下顺序进行加载各个子模块
        self.__sub_modules.update(modules)
        
    # 根据 kind, name 自动获取系统配置信息
    def _read_config(self) -> object:
        return config.get_system_module(self.__kind, self.__name)

    ''' ----- Getter ----- '''
    @property
    def is_running(self) -> bool:
        return self.__is_running

    @property
    def kind(self) -> str:
        return self.__kind
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def kind_with_name(self, format: str="{kind} ({name})") -> str:
        return format.format(kind=self.__kind, name=self.__name)

    
