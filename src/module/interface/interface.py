from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Self, Callable
from threading import Thread

from utils.config import config

class ModuleInterface(metaclass=ABCMeta):
    def __init__(self, name: str):
        """ 初始化函数

        Args:
            name (str): 模块名称
            kind (str): 模块具体对应的类型
            runKind (str): 
        """
        # 模块的基本信息
        self.__is_running = False
        self.__name = name
        # self.__kind = kind

        # 线程相关
        self.__threads: List[Thread] = []        

        # 子模块相关的属性
        # self.__sub_modules_list: List[str|Dict[str, str]] = []
        # self._sub_modules: Dict[str, Self] = {}
        # self.__height = 0

    # 该函数主要由模块管理器统一进行管理，统一进行更新
    @abstractmethod
    def _load_config(self):
        # 需要每次更新配置文件以保证最新
        pass

    # 如果验证成功则直接通过，失败则 raise 错误
    # 主要是用于是否能够正常启动模块
    def check(self) -> Tuple[bool, Exception]:
        return (True, None)

    # 启动模块单元
    @abstractmethod
    def start(self):
        ...

    # 停止模块单元
    @abstractmethod
    def stop(self):
        ...
        
    # 根据 kind, name 自动获取系统配置信息
    def _read_config(self) -> object:
        return config.get_system_module(self.info.name, self.info.kind)
    
    # 开辟一个线程用于处理
    def _make_thread(self, target: Callable):
        thread = Thread(target=target)
        self.__threads.append(thread)
        thread.start()

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
    def label(self, format: str="{name} [{kind}]") -> str:
        return format.format(kind=self._info.kind, name=self._info.name)
    
    ''' ----- Setter -----'''
    # def set_height(self, height: int):
    #     self.__height = height

    # 由配置文件自动设置，不需要手动配置
    # def _set_sub_modules(self, modules: List[str]):
    #     # Notice: 模块启动时也会按照如下顺序进行加载各个子模块
    #     self.__sub_modules_list = modules

    
