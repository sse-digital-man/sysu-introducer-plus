from abc import abstractmethod
from typing import List, Tuple, Callable, Self
from threading import Thread

from .interface import ModuleInterface
from .manager import manager
from .info import ModuleInfo

from utils.config import config

VIRTUAL = "virtual"
BASIC = "basic"
NULL = "null"

class BasicModule(ModuleInterface):
    def __init__(self, name: str):
        """ 初始化函数

        Args:
            name (str): 模块名称
        """
        # 模块的基本信息
        super().__init__(name)

        # 线程相关
        self.__threads: List[Thread] = []  

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
    def start(self):
        # 1. 更新配置信息
        self._load_config()

        # TODO: 显示模块加载情况
        if self._info.depth == 0:
            print("正在启动模块: ")
        print(self._info.depth * "    " + self.label)

        # 2. 启动子模块
        for module in self._sub_module_list:
            if module is not None:
                module.start()

        # 模块自检
        (flag, e) = self.check()
        if not flag:
            raise e if e!= None else SystemError(self.name, "check error")
        # 3. 运行模块自定义处理逻辑
        self._before_running()
        
        # Notice: TODO: 只有所有程序启动成功之后 才能更新状态

        if self._info.depth == 0:
            print("模块启动成功")

        # 4. 钩子函数
        self._after_running()

    # 停止模块单元
    def stop(self):
        # 1. TODO: 先设置标志位

        # 2. 关闭内部的线程处理
        for thread in self.__threads:
            thread.join()

        # 3. 关闭子线程
        for module in self._sub_module_list:
            if module is not None:
                module.stop()
        
    # 根据 kind, name 自动获取系统配置信息
    def _read_config(self) -> object:
        return config.get_system_module(self._info.name, self._info.kind)
    
    # 开辟一个线程用于处理
    def _make_thread(self, target: Callable):
        thread = Thread(target=target)
        self.__threads.append(thread)
        thread.start()
    
    ''' ----- Hook -----'''
    
    def _before_running(self):
        pass

    def _after_running(self):
        pass

    ''' ----- Getter ----- '''
    # 获取当前的模块信息
    @property
    def _info(self) -> ModuleInfo:
        return manager.info(self.name)
    
    # 获取子模块的对象
    def _sub_module(self, name: str) -> Self:
        if name not in manager.info(self.name).modules:
            raise FileNotFoundError(f"{name} is not in {self.name}")

        return manager.object(name)

    # 获取子模块对象的列表
    @property
    def _sub_module_list(self) -> List[Self]:
        sub_module_names = manager.info(self.name).modules
        return [manager.object(name) for name in sub_module_names]
    
    ''' ----- Setter -----'''