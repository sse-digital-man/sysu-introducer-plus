from abc import ABCMeta, abstractmethod
from typing import Tuple

class ModuleInterface(metaclass=ABCMeta):
    def __init__(self, name: str):
        """ 初始化函数

        Args:
            name (str): 模块名称
            kind (str): 模块具体对应的类型
            runKind (str): 
        """
        # 模块的基本信息
        self.__name = name

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
    
    ''' ----- Getter ----- '''
    @property
    @abstractmethod
    def kind(self) -> str:
        ...
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def label(self, format: str="{alias} ({kind})") -> str:
        ...
    
    @property
    @abstractmethod
    def is_running(self) -> bool:
        ...