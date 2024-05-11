from abc import abstractmethod
from typing import List, Tuple, Dict, Callable, Self
from threading import Thread

from .interface import ModuleInterface
from .manager import manager
from .info import ModuleInfo, ModuleStatus
from .log import ModuleStatusLog

from utils.config import config

VIRTUAL = "virtual"
BASIC = "basic"
NULL = "null"

class BasicModule(ModuleInterface):
    def __init__(self, name: str):
        """ 初始化函数，注意不要在此处编写过多地初始化操作

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
    def start(self, with_sub_modules: bool=True):
        # 0. FIXME: 如果该模块已经运行则无需运行
        if self._is_ready:
            return

        # 1. 首先启动启动子模块
        self._before_starting()
        self._set_status(ModuleStatus.Starting)

        if with_sub_modules: 
            for module in self._sub_module_list:
                if module is not None:
                    module.start()

        # 2. 更新配置信息
        self._load_config()

        # 3. 模块自检
        (flag, e) = self.check()
        if not flag:
            raise e if e!= None else SystemError(self.name, "check error")
        
        # 4. 运行模块自定义处理逻辑
        self._before_started()
        
        # 5. 钩子函数
        self._set_status(ModuleStatus.Started)
        self._after_started()

    # 停止模块单元
    def stop(self):
        # 1. TODO: 先设置标志位
        self._set_status(ModuleStatus.Stopping)

        # 2. 关闭内部的线程处理
        for thread in self.__threads:
            thread.join()

        # 3. 关闭子线程
        for module in self._sub_module_list:
            if module is not None:
                module.stop()

        self._set_status(ModuleStatus.Stopped)

    def _read_config(self) -> Dict:
        return config.get(self.info.name, self.info.kind)
        
    # 开辟一个线程用于处理
    def _make_thread(self, target: Callable):
        thread = Thread(target=target)
        self.__threads.append(thread)
        thread.start()
    
    ''' ----- Hook -----'''
    
    def _before_starting(self):
        pass

    def _before_started(self):
        pass

    def _after_started(self):
        pass

    ''' ----- Getter ----- '''
    @property
    def kind(self) -> str:
        return self.info.kind; 

    # 获取当前的模块信息
    @property
    def info(self) -> ModuleInfo:
        return manager.info(self.name)
    
    @property
    def status(self) -> ModuleStatus:
        return self.info.status
    
    @property
    def is_running(self) -> bool:
        return self.status is ModuleStatus.Started
    
    @property
    def _is_ready(self) -> bool:
        """判断当前模块是否满足线程的运行条件, 主要模块内部可控制线程运行

        Returns:
            bool: 结果
        """
        
        return self.status in [ModuleStatus.Started, ModuleStatus.Starting]

    # 获取子模块的对象
    def _sub_module(self, name: str) -> Self:
        if name not in manager.info(self.name).modules:
            raise FileNotFoundError(f"{name} is not in {self.name}")

        return manager.object(name)
    
    @property
    def sub_module_list(self) -> List[str]:
        return manager.info(self.name).modules
    
    # 获取子模块对象的列表
    @property
    def _sub_module_list(self) -> List[Self]:
        sub_module_names = manager.info(self.name).modules
        return [manager.object(name) for name in sub_module_names]
    
    ''' ----- Setter -----'''
    def _set_status(self, status: ModuleStatus):
        self.info.status = status

        manager.log(ModuleStatusLog(self.name, status))