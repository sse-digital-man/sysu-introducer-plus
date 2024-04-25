from abc import ABCMeta, abstractmethod
from typing import List, Dict, Self, Callable
from importlib import import_module
from threading import Thread


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

        # start 函数的逻辑（每个模块需要自定义）
        self._startup_func = None
        self._startup_thread = None

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
    @abstractmethod
    def check(self) -> bool:
        ...

    # 启动模块单元
    def start(self):
        # 更新
        self._load_config()
        self._load_sub_modules()

        # TODO: 显示模块加载情况
        if self.__height == 0:
            print("正在加载模块: ")
        print(self.__height * "    " + self.label)

        # 循环启动各个子模块
        for module in self._sub_modules.values():
            if module is None:
                continue

            if not module.check():
                print(module.name, "check error")
                return
            module.start()

        # 运行模块自定义处理逻辑
        if self._startup_thread != None:
            self._startup_thread.start()
        elif self._startup_func != None:
            self._startup_func()

        # Notice: 只有所有程序启动成功之后 才能更新状态
        self.__is_running = True

    # 停止模块单元
    def stop(self):
        try:
            for module in self.__modules.values():
                module.stop()

            if self._startup_thread != None:
                self._startup_thread.join()
        except Exception:
            pass
        finally:
            # 无论如何 最后都需要更新状态
            self.__is_running = False

    
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

    def _set_startup_func(self, startup_func: Callable, with_thread: bool=True):
        """设置模块自定义

        Args:
            startup_func (Callable): _description_
            with_thread (bool, optional): _description_. Defaults to True.
        """

        self._startup_func = startup_func
        if with_thread:
            self._startup_thread = Thread(target=startup_func)
        else:
            self._startup_thread = None

    
