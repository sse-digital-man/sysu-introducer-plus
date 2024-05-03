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
            kind (str): 模块具体对应的类型
            runKind (str): 
        """
        # 模块的基本信息
        super().__init__(name)
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
    def start(self):
        # 更新
        self._load_config()

        # TODO: 显示模块加载情况
        if self._info.depth == 0:
            print("正在加载模块: ")
        print(self._info.depth * "    " + self.label)

        self._before_load_sub_modules()

        # 循环启动各个子模块
        # self._load_sub_modules()

        self._after_load_sub_modules()

        for module in self._modules:
            if module is None:
                continue

            module.start()

        # 运行模块自定义处理逻辑
        self._before_running()

        # 模块自检
        (flag, e) = self.check()
        if not flag:
            raise e if e!= None else SystemError(self.name, "check error")
        
        # Notice: 只有所有程序启动成功之后 才能更新状态
        self.__is_running = True

        if self._info.depth == 0:
            print("模块加载成功")

        # 钩子函数
        self._after_running()

    # 停止模块单元
    def stop(self):
        # 无论如何 最后都需要更新状态
        self.__is_running = False

        # 先关闭内部的线程处理
        for thread in self.__threads:
            thread.join()

        # for module in self._sub_modules.values():
        #     if module is not None:
        #         module.stop()
    
    # 添加子模块
    # def _load_sub_modules(self):
    #     modules = self.info.modules

    #     for module_info in modules:
    #         module_object = import_module_dynamic(module_info)

        # print("load: ", self._sub_modules)
        
    # 根据 kind, name 自动获取系统配置信息
    def _read_config(self) -> object:
        return config.get_system_module(self._info.name, self._info.kind)
    
    # 开辟一个线程用于处理
    def _make_thread(self, target: Callable):
        thread = Thread(target=target)
        self.__threads.append(thread)
        thread.start()
    
    ''' ----- Hook -----'''
    
    def _before_load_sub_modules(self):
        pass

    def _after_load_sub_modules(self):
        pass

    def _before_running(self):
        pass

    def _after_running(self):
        pass

    ''' ----- Getter ----- '''
    def _module(self, name: str) -> Self:
        # from .manager import manager
        return manager.object(name)
    
    @property
    def _info(self) -> ModuleInfo:
        # from .manager import manager
        return manager.info(self.name)
    
    @property
    def _modules(self) -> List[Self]:
        # from .manager import manager
        return [manager.object(name) for name in manager.info(self.name).modules]
    
    ''' ----- Setter -----'''
    # def set_height(self, height: int):
    #     self.__height = height

    # 由配置文件自动设置，不需要手动配置
    # def _set_sub_modules(self, modules: List[str]):
    #     # Notice: 模块启动时也会按照如下顺序进行加载各个子模块
    #     self.__sub_modules_list = modules

    
