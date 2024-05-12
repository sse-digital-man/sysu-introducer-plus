from typing import Dict, List, Tuple, Callable
from importlib import import_module

from utils.file import load_json

from . import BasicModule
from .info import ModuleInfo, ModuleStatus

from .log.interface import ModuleLog, ModuleCallback
from .log import ModuleStatusLog

CONFIG_PATH = "src/modules.json"

NULL = "null"
BASIC = "basic"

LogCallBack = Callable[[ModuleLog], None]

def generate_name(name: str, kind: str):
    if kind == None: kind = "basic"

    return kind.title() + name.title()

class ModuleManageCell:
    def __init__(self, info: ModuleInfo):
        self.info = info
        self.status: ModuleStatus = ModuleStatus.NotLoaded

        # 模块对象指针
        self.module: BasicModule = None

        # 记录管理单元的父子关系
        self.sup: ModuleManageCell | None = None
        self.sub: Dict[str, ModuleManageCell] = {}

    @property
    def name(self) -> str:
        return self.info.name

    def inject(self, log: ModuleCallback):
        """将模块管理单元中包含的信息注入到其模块对象中

        """
        
        if self.module == None:
            return
        
        submodules = { name: child_cell.module for name, child_cell in self.sub.items() }
        self.module.inject(self.info.name, self.info.kind, submodules, log)

class ModuleManager:
    def __init__(self):
        self.__module_cells: Dict[str, ModuleManageCell] = {}
        self.__is_loaded = False
        self.__log_callback: None | LogCallBack = None
        
        self.__load_modules()

    def __load_modules(self):
        if self.__is_loaded:
            return

        # 1. 从配置文件中加载模块信息
        modules_info: Dict[str, Dict] = load_json(CONFIG_PATH)
        for (name, content) in modules_info.items():
            info = ModuleInfo(name, content["alias"], 
                content.get("kinds", []),
                content.get("default", "basic"),
                content.get("notNull", True),
                content.get("path", ""),
                content.get("modules", [])
            )
            
            self.__module_cells[name] = ModuleManageCell(info)

        # 2. 验证模块情况
        self.__check_modules()

        # 3. 验证实现类型
        self.__check_kinds()

        # 3. 加载模块对象
        for (name, cell) in self.__module_cells.items():
            module_object = self.__dynamic_import_module(name)
            # 如果需要加载的模块类型为空，则表示仍未加载
            if module_object != None:
                cell.module = module_object()
                cell.status = ModuleStatus.Stopped

        # 4. 加载父子模块指针
        for (name, cell) in self.__module_cells.items():
            if cell.module == None:
                continue

            # 遍历加载所有子模块
            for submodule in cell.info.sub:
                # 在父模块中添加子模块
                cell.sub[submodule] = self.__module_cells[submodule]
                # 在子模块中添加父模块
                self.__module_cells[submodule].sup = cell
        
        # 5. 依赖注入
        for cell in self.__module_cells.values():
            cell.inject(self.log)
            
        self.__is_loaded = True

    def __check_modules(self):
        # 验证所有子模块是否存在, 并加载子模块的嵌套深度
        in_degree = dict.fromkeys(self._module_name_list, 0)

        for cell in self.__module_cells.values():
            for submodule in cell.info.sub:
                sub_cell =  self.__module_cells.get(submodule, None)
                if sub_cell is None:
                    raise FileNotFoundError(f"{submodule} in {cell.name} not found")
                
                in_degree[submodule] = in_degree.get(submodule) + 1

                # 设置 ModuleInfo 中子节点指向父节点的指针
                sub_cell.info.sup = cell.name

        # 如果没有入度为 0 的节点，说明存在循环依赖
        queue = []

        for name in self._module_name_list:
            if in_degree[name] == 0:
                queue.append(name)

        if len(queue) == 0:
            raise ImportError(f"circular dependency between modules") 
        
        # 使用 BFS 计算所有节点深度
        depth = 0
        while len(queue) > 0:
            size = len(queue)

            for _ in range(size):
                name = queue.pop(0)
                info = self.__module_cells[name].info
                info.depth = depth

                for submodule in info.sub:
                    in_degree[submodule] -= 1

                    if in_degree[submodule] == 0:
                        queue.append(submodule)

            depth += 1

    # 子模块
    def __dynamic_import_module(self, name: str, kind: str=None):
        cell = self.__module_cells[name]
        info = cell.info

        # 1. 收集包路径
        names: List[str] = []
        
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
        for cell in self.__module_cells.values():
            info = cell.info

            # 如果当前实现类型是基本类型，则只有一种实现类型，不需要校验
            # if info.kind == BASIC:
            #     continue
            
            # 验证当前实现是否存咋支持的 kinds 中
            if info.kind not in info.kinds:
                raise ValueError(f"the kind '{info.kind}' is not supported in {info.name}")                

            # 验证对应子实现
            for kind in info.kinds:
                try: 
                    # 如果能导入说明存在
                    self.__dynamic_import_module(info.name, kind)
                except ImportError:
                    raise ValueError(f"the kind '{kind}' does not exist in {info.name}")


    def log(self, log: ModuleLog):
        # TODO: 发送日志后的处理函数
        
        if self.__log_callback is not None:
            self.__log_callback(log)

    ''' ----- 模块控制 ----- '''

    # 启动模块单元
    def start(self, name: str, with_submodules: bool=True) -> Tuple[bool, ModuleStatus]:
        """启动模块

        Args:
            name (str): 模块名称
            with_submodules (bool, optional): 是否自动运行子模块. Defaults to True.

        Returns:
            bool: 是否运行成功，当前的状态（运行成功为None）
        """

        cell = self.__module_cells.get(name)
        if cell == None:
            raise FileNotFoundError(f"module '{name}' not found")
        
        # 0. 如果当前模块状态不是在停止状态 则不能停止
        cur_status = cell.status
        if cur_status != ModuleStatus.Stopped:
            return False, cur_status

        # 1. 首先启动启动子模块
        module = cell.module
        module._before_starting()
        self._update_status(cell, ModuleStatus.Starting)

        if with_submodules: 
            for sub_name, submodule in cell.sub.items():
                if submodule != None: self.start(sub_name)

        # 2. 更新配置信息
        module._load_config()

        # 3. 模块自检
        (flag, e) = module.check()
        if not flag:
            raise e if e!= None else SystemError(self.name, "check error")
        
        # 4. 运行模块自定义处理逻辑
        module._before_started()
        
        # 5. 钩子函数
        self._update_status(cell, ModuleStatus.Started)
        module._after_started()

        return True, None

    # 停止模块单元
    def stop(self, name: str) -> bool:
        """停止模块

        Args:
            name (str): 模块名称

        Returns:
            bool: 是否运行成功，当前的状态（运行成功为None）
        """

        cell = self.__module_cells.get(name)
        if cell == None:
            raise FileNotFoundError(f"module '{name}' not found")

        cur_status = cell.status
        if cur_status != ModuleStatus.Started:
            return False, cur_status

        # 1. 先设置标志位
        self._update_status(cell, ModuleStatus.Stopping)

        # module = cell.module

        # # 2. 关闭内部的线程处理
        # for thread in module.__threads:
        #     thread.join()

        # 3. 关闭子线程
        for sub_name, submodule in cell.sub.items():
            if submodule != None: self.stop(sub_name)
        self._update_status(cell, ModuleStatus.Stopped)

        return True, None

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
        
        cell = self.__module_cells.get(name)
        if cell == None:
            raise FileNotFoundError(f"module '{name}' not found")
        
        # 判断模块状态是否可切换
        cur_status = cell.status
        if not ModuleStatus.can_change(cur_status):
            # raise RuntimeError(f"module is '{info.status.name}', so it can't be changed", info.status)
            return False, cur_status
        
        # 如果置空，则需要清空记录
        info = cell.info
        if kind not in info.kinds:
            raise ValueError(f"the kind of implement '{kind}' is not supported ")   
        # 模块不限定 basic 只存在一种实现类型，其只作为最基本的实现类型
        # elif kind == BASIC:
        #     if len(info.kinds) != 0:
        #         raise ValueError(f"the module '{name}' is not single implementation")
        #     return 

        info.kind = kind
        if kind == NULL:
            self._update_status(cell, ModuleStatus.NotLoaded)
            cell.module = None
        else:
            self._update_status(cell, ModuleStatus.Stopped)
            
            # 1. 使用动态导入模块
            module: BasicModule = self.__dynamic_import_module(name, kind)()
            # 2. 设置模块
            cell.module = module
            # 3. 依赖注入
            cell.inject(self.log)

        # 2. 重新设置父模块中的指针
        sup_name = cell.sup.name
        self.__module_cells[sup_name].sub[name] = cell

        # FIXME: 使用抛出异常解决运行不成功的问题
        return True, None
    
    def check_exist(self, name: str) -> bool:
        """验证模块是否存在

        Args:
            name (str): 模块名称

        Returns:
            bool: 是否存在
        """
        return name in self.__module_cells.keys()

    ''' ----- Getter ----- '''

    def info(self, name: str) -> ModuleInfo | None:
        cell = self.__module_cells.get(name, None)

        return cell.info if cell != None else None
    
    def module(self, name: str) -> BasicModule | None:
        cell = self.__module_cells.get(name, None)
        
        return cell.module if cell != None else None

    @property
    def _module_name_list(self) -> List[str]:
        return self.__module_cells.keys()
    
    @property
    def module_info_list(self) -> List[Dict]:
        """列表组成 name, alias, kind, status

        Returns:
            List[Dict]: 信息的列表
        """

        info_list = []
        for cell in self.__module_cells.values():
            info_dict = cell.info.to_dict()
            # 添加状态信息
            info_dict["status"] = cell.status
            info_list.append(info_dict)

        return info_list
    
    ''' ----- Setter -----'''

    def _update_status(self, cell: ModuleManageCell, new_status: ModuleStatus):
        name = cell.info.name

        # Notice: 必须使用该函数进行更新状态
        cell.status = new_status
        cell.module.update_status(new_status)
        self.log(ModuleStatusLog(name, new_status))

    def set_log_callback(self, callback: LogCallBack):
        self.__log_callback = callback

# Notice: 使用单例模式使用模块管理器
MANAGER = ModuleManager()