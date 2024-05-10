from typing import Dict, List, Tuple, Callable
from importlib import import_module

from utils.file import load_json
from .info import ModuleInfo, ModuleStatus
from .interface import ModuleInterface
from .log.interface import ModuleLog

CONFIG_PATH = "src/modules.json"

NULL = "null"
BASIC = "basic"

LogCallBack = Callable[[ModuleLog], None]

def generate_name(name: str, kind: str):
    if kind == None: kind = "basic"

    return kind.title() + name.title()

class ModuleManager:
    def __init__(self):
        self.__module_name_list: List[str] = []
        self.__module_info_list: Dict[str, ModuleInfo] = {}
        self.__module_object_list: Dict[str, ModuleInterface] = {}

        self.__is_loaded = False

        self.__log_callback: None | LogCallBack = None

    def load_modules(self):
        if self.__is_loaded:
            return

        # 1. 从配置文件中加载模块信息
        modules_info: Dict[str, Dict] = load_json(CONFIG_PATH)
        self.__module_name_list = list(modules_info.keys())

        for (name, content) in modules_info.items():
            self.__module_info_list[name] = \
                ModuleInfo(name, content["alias"], 
                    content.get("kinds", []),
                    content.get("default", "basic"),
                    content.get("notNull", True),
                    content.get("path", ""),
                    content.get("modules", [])
                )
            
        # 2. 验证模块情况
        self.__check_modules()

        # 3. 验证实现类型
        self.__check_kinds()

        # 3. 加载模块对象
        for name in self.__module_name_list:
            module_object =  self.__dynamic_import_module(name)
            # 如果需要加载的模块类型为空，则表示仍未加载
            if module_object != None:
                self.__module_object_list[name] = module_object()
                self.__module_info_list[name].status = ModuleStatus.Stopped

        self.__is_loaded = True

    def __check_modules(self):
        # 验证模块是否存在, 并加载子模块的嵌套深度
        in_degree = dict.fromkeys(self.__module_name_list, 0)

        for info in self.__module_info_list.values():
            for sub_name in info.modules:
                if self.__module_info_list.get(sub_name) is None:
                    raise FileNotFoundError(f"{sub_name} in {info.name} not found")
                
                in_degree[sub_name] = in_degree.get(sub_name) + 1

        names = list(self.__module_name_list)
        queue = []

        for name in names:
            if in_degree[name] == 0:
                queue.append(name)

        # 如果没有入度为 0 的节点，说明存在循环依赖
        if len(queue) == 0:
            raise ValueError(f"circular dependency between modules") 
        
        # 使用 BFS 计算所有节点深度
        depth = 0
        while len(queue) > 0:
            size = len(queue)

            for _ in range(size):
                name = queue.pop(0)
                info = self.__module_info_list[name]
                info.depth = depth

                for sub_name in info.modules:
                    in_degree[sub_name] -= 1

                    if in_degree[sub_name] == 0:
                        queue.append(sub_name)

            depth += 1

    # 子模块
    def __dynamic_import_module(self, name: str, kind: str=None):
        # 1. 收集包路径
        names: List[str] = []

        info = self.info(name)
        if len(info.path) != 0:
            names.append(info.path)
        names.append(info.name)

        # 如果传输进来的实现类型为空，则读取 kind
        if kind == None:
            kind = info.kind

        if kind == NULL:
            return None
        elif kind != BASIC:
            names.append(kind)

        class_name = generate_name(name,kind)

        return import_module(".".join(names)).__getattribute__(class_name)

    def __check_kinds(self):
        for info in self.__module_info_list.values():
            # 如果当前实现类型是基本类型，则只有一种实现类型，不需要校验
            if info.kind == BASIC:
                continue
            
            # 验证当前实现是否存咋支持的 kinds 中
            if info.kind not in info.kinds:
                raise ValueError(f"the kind of implement '{kind}' is not supported ")                

            # 验证对应子实现
            for kind in info.kinds:
                try: 
                    # 如果能导入说明存在
                    self.__dynamic_import_module(info.name, kind)
                except ImportError:
                    raise ValueError(f"the kind of implement '{kind}' does not exist")


    def log(self, log: ModuleLog):
        # TODO: 发送日志后的处理函数
        
        if self.__log_callback is not None:
            self.__log_callback(log)

    def change_module_kind(self, name: str, kind: str) -> Tuple[bool, ModuleStatus]:
        """切换模块的实现类型，并返回是否切换成功

        Args:
            name (str): 模块名称
            kind (str): 模块实现类型

        Raises:
            FileNotFoundError: 模块不存在
            ValueError: 模块实现类型不支持

        Returns:
            Tuple[bool, ModuleStatus]: 是否切换成功、当前状态（切换成功为空）
        """
        info = self.__module_info_list.get(name, None)

        if info is None:
            raise FileNotFoundError(f"module '{name}' not found")
        
        # 判断模块状态是否可切换
        cur_status = info.status
        if not ModuleStatus.can_change(cur_status):
            # raise RuntimeError(f"module is '{info.status.name}', so it can't be changed", info.status)
            return False, cur_status
        
        # 如果置空，则需要清空记录
        if kind == NULL:
            info.kind = NULL
            info.status = ModuleStatus.NotLoaded
            self.__module_object_list[name] = None
            return True, None
        # 模块不限定 basic 只存在一种实现类型，其只作为最基本的实现类型
        # elif kind == BASIC:
        #     if len(info.kinds) != 0:
        #         raise ValueError(f"the module '{name}' is not single implementation")
        #     return 
        elif kind not in info.kinds:
            raise ValueError(f"the kind of implement '{kind}' is not supported ")      

        # 使用动态导入模块
        info.kind = kind
        self.__module_object_list[name] = self.__dynamic_import_module(name, kind)()

        # FIXME: 使用抛出异常解决运行不成功的问题
        return True, None

    ''' ----- Getter ----- '''
    
    def info(self, name: str) -> ModuleInfo:
        return self.__module_info_list.get(name)
    
    def object(self, name: str) -> ModuleInterface:
        return self.__module_object_list.get(name)
    
    @property
    def module_info_list(self) -> List[Dict]:
        """列表组成 name, alias, kind, status

        Returns:
            List[Dict]: 信息的列表
        """

        list = []
        for info in self.__module_info_list.values():
            list.append(info.to_dict())

        return list
    
    ''' ----- Setter -----'''
    
    def set_log_callback(self, callback: LogCallBack):
        self.__log_callback = callback

    ''' ----- Debug ----- '''

    # 用于表格化输出所有模块信息
    def __show_as_table(self) -> str:
        from tabulate import tabulate

        header = ["name", "alias", "kind", "path", "modules", "depth"]
        
        rows = [
            [info.name, info.alias, info.kind, info.path, ", ".join(info.modules), info.depth] 
            for info in self.__module_info_list.values()
        ]

        return tabulate(rows, header, tablefmt="github")


# Notice: 使用单例模式使用模块管理器
manager = ModuleManager()