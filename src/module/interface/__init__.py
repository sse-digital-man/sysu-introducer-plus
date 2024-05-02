from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Self, Callable
from importlib import import_module
from threading import Thread

from .container import ModuleContainer

from utils.config import config

VIRTUAL = "virtual"
BASIC = "basic"
NULL = "null"


def generate_name(name: str, kind: str):
    if kind == None: kind = "basic"

    return kind.title() + name.title()

def import_module_dynamic(module: str | Dict[str, str]):
    # 1. 收集包路径
    names: List[str] = []

    # 2. 设置基本路径，模块名的路径
    if isinstance(module, str):
        names.append("module")
        names.append(module)
        name = module
    else:
        path = module["path"]
        name = module['name']

        if path is not None:
            names.append(path)
        names.append(name)

    # 3. 设置模块的类型
    try:
        kind = config.get_use_module(name)  
        if isinstance(kind, str): 
            names.append(kind) 
    except:
        kind = "basic"

    if kind == "null":
        return (name, None)

    class_name = generate_name(name, kind)

    # print(".".join(names), class_name)
    return (name, import_module(".".join(names)).__getattribute__(class_name))


class ModuleInterface(metaclass=ABCMeta):
    container = ModuleContainer()


    def __init__(self, name: str, kind: str=BASIC):
        """ 初始化函数

        Args:
            name (str): 模块名称
            kind (str): 模块具体对应的类型
            runKind (str): 
        """
        # 模块的基本信息
        self.__is_running = False
        self.__name = name
        self.__kind = kind

        # 线程相关
        self.__threads: List[Thread] = []        

        # 子模块相关的属性
        self.__sub_modules_list: List[str|Dict[str, str]] = []
        self._sub_modules: Dict[str, Self] = {}
        self.__height = 0

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
        if self.__height == 0:
            print("正在加载模块: ")
        print(self.__height * "    " + self.label)

        self._before_load_sub_modules()

        # 循环启动各个子模块
        self._load_sub_modules()

        self._after_load_sub_modules()

        for module in self._sub_modules.values():
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

        if self.__height == 0:
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

        for module in self._sub_modules.values():
            if module is not None:
                module.stop()
    
    # 添加子模块
    def _load_sub_modules(self):
        modules = self.__sub_modules_list

        for module_info in modules:
            (name, module_object) = import_module_dynamic(module_info)

            module = module_object() if module_object != None else None
            self._sub_modules[name] = module
            if module is not None:
                module.set_height(self.__height + 1)

        # print("load: ", self._sub_modules)
        
    # 根据 kind, name 自动获取系统配置信息
    def _read_config(self) -> object:
        return config.get_system_module(self.__name, self.__kind)
    
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
        return format.format(kind=self.__kind, name=self.__name)
    
    ''' ----- Setter -----'''
    def set_height(self, height: int):
        self.__height = height

    def _set_sub_modules(self, modules: List[str]):
        # Notice: 模块启动时也会按照如下顺序进行加载各个子模块
        self.__sub_modules_list = modules

    
