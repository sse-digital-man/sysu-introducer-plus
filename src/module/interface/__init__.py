from abc import abstractmethod, ABCMeta
from typing import List, Dict, Tuple, Callable, Self
from threading import Thread

from .info import ModuleStatus

from utils.config import config

class BasicModule(metaclass=ABCMeta):
    def __init__(self):
        """ 初始化函数，注意不要在此处编写过多地初始化操作

        Args:
            name (str): 模块名称
        """
        # 模块的基本信息
        super().__init__()

        # 依赖注入
        self.__name = None
        self.__kind = None
        self.__status = ModuleStatus.NotLoaded
        self.__sub_modules: Dict[str, Self | None]

        self.__hasInjected = False

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

    def _read_config(self) -> object:
        return config.get(self.name, self.kind)
        
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
    def name(self) -> str:
        return self.__name

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def status(self) -> ModuleStatus:
        return self.__status
    
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
        try:
            # Notice: 不能直接比较 None, 因为未加载的模块返回为空
            return self.__sub_modules[name]
        except:
            raise FileNotFoundError(f"{name} is not in {self.name}")
    
    @property
    def sub_module_list(self) -> List[str]:
        return list(self.__sub_modules.keys())
    
    # 获取子模块对象的列表
    @property
    def _sub_module_list(self) -> List[Self]:
        return list(self.__sub_modules.values())
    
    ''' ----- Setter -----'''


    ''' ----- 管理器依赖注入 ----- '''

    def inject(self, name: str, kind: str, sub_modules: Dict[str, Self]):
        """管理器初次注入信息

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型
            sub_modules (Dict[str, Self]): 子模块对象指针
        """

        if self.__hasInjected:
            raise RuntimeError("object of module has been injected")

        self.__name = name
        self.__kind = kind
        self.__sub_modules = sub_modules

        self.__hasInjected = True

    def update_status(self, status: ModuleStatus):
        self.__status = status

    def update_sub_module(self, sub_module: Self):
        self.__sub_modules[sub_module.name] = sub_module

        