import sys
from typing import Dict, List, Tuple, Callable
from importlib import import_module

from utils.file import load_json
from utils import error

from message import Message
from . import BasicModule, BooterInterface
from .info import ModuleInfo, ModuleStatus

from .log.interface import ModuleLog, ModuleCallback
from .log import ModuleStatusLog

CONFIG_PATH = "modules.json"

NULL = "null"
BASIC = "basic"

LogCallBack = Callable[[ModuleLog], None]


def generate_name(name: str, kind: str):
    if kind is None:
        kind = "basic"

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

    def inject(self, log: ModuleCallback):
        """将模块管理单元中包含的信息注入到其模块对象中"""

        if self.module is None:
            return

        submodules = {name: child_cell.module for name, child_cell in self.sub.items()}
        self.module.inject(self.info.name, self.info.kind, submodules, log)

    @property
    def name(self) -> str:
        return self.info.name

    @property
    def is_null(self) -> bool:
        return self.module is None


class ModuleManager:
    def __init__(self):
        self.__module_cells: Dict[str, ModuleManageCell] = {}
        # Notice: 模块依赖树的根节点必须是一个 Booter
        self.__booter_cell: ModuleManageCell = None

        self.__is_loaded = False
        self.__log_callback: None | LogCallBack = None

        self.__load_modules()

    def __load_modules(self):
        if self.__is_loaded:
            return

        # 1. 从配置文件中加载模块信息
        modules_info: Dict[str, Dict] = load_json(CONFIG_PATH)
        for name, content in modules_info.items():
            info = ModuleInfo(
                name,
                content["alias"],
                content.get("kinds", []),
                content.get("default", "basic"),
                content.get("notNull", True),
                content.get("path", ""),
                content.get("modules", []),
            )

            self.__module_cells[name] = ModuleManageCell(info)

        # 2. 验证模块情况
        self.__check_modules()

        # 3. 验证实现类型
        for cell in self.__module_cells.values():
            info = cell.info

            # 验证所支持的模块是否实现
            for kind in info.kinds:
                self.__dynamic_import_module(info.name, kind)

            # 验证当前实现类型
            self._check_kind_exist(cell, info.kind)

        # 3. 加载模块对象
        for name, cell in self.__module_cells.items():
            module_object = self.__dynamic_import_module(name)
            # 如果需要加载的模块类型为空，则表示仍未加载
            if module_object is not None:
                cell.module = module_object()
                cell.status = ModuleStatus.Stopped
            else:
                cell.module = None
                cell.status = ModuleStatus.NotLoaded

        # 4. 加载父子模块指针
        for name, cell in self.__module_cells.items():
            if cell.module is None:
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

    # 子模块
    def __dynamic_import_module(self, name: str, kind: str = None):
        cell = self.__module_cells[name]
        info = cell.info

        # 1. 收集包路径
        names: List[str] = []

        names.append("module")
        if len(info.path) != 0:
            names.append(info.path)
        names.append(info.name)

        # 如果传输进来的实现类型为空，则读取 kind
        if kind is None:
            kind = info.kind

        if kind == NULL:
            return None
        if kind != BASIC:
            names.append(kind)

        class_name = generate_name(name, kind)

        try:
            return getattr(import_module(".".join(names)), class_name)
        except ModuleNotFoundError as e:
            path = str(e.name)

            # 当导入 module 模块时发生错误，则说明未实现
            if path.startswith("module"):
                names = path.split(".")
                name = names[-2]
                kind = names[-1] if len(names) > 2 else "basic"

                raise error.ModuleLoadError(
                    f"the kind '{kind}' in {name} is not implemented"
                )

            raise e

    def __check_modules(self):
        # 验证所有子模块是否存在, 并加载子模块的嵌套深度
        in_degree = dict.fromkeys(self._module_name_list, 0)

        for cell in self.__module_cells.values():
            for submodule in cell.info.sub:
                sub_cell = self.__module_cells.get(submodule, None)
                if sub_cell is None:
                    raise FileNotFoundError(f"{submodule} in {cell.name} not found")

                in_degree[submodule] = in_degree.get(submodule) + 1

                # 设置 ModuleInfo 中子节点指向父节点的指针
                sub_cell.info.sup = cell.name

        # 添加入度为0的
        queue = []

        for name in self._module_name_list:
            if in_degree[name] == 0:
                queue.append(name)

        # 如果没有入度为 0 的节点，说明存在循环依赖
        if len(queue) == 0:
            raise error.ModuleLoadError("circular dependency between modules")
        # 出现多个booter
        if len(queue) != 1:
            raise error.ModuleLoadError("multiple root module are loaded")

        self.__booter_cell = self.__module_cells[queue[0]]

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

    def _check_module_exist(self, name: str) -> bool:
        """验证模块是否存在

        Args:
            name (str): 模块名称

        Returns:
            bool: 是否存在
        """
        if name not in self.__module_cells:
            raise FileNotFoundError(f"module '{name}' not found")

    def _check_kind_exist(self, cell: ModuleManageCell, kind: str):
        """验证模块实现是否存在，不传入特定实现类型名称则比较 ModuleInfo 中的实现类型

        Args:
            cell (ModuleManageCell): 模块管理单元
            kind (str, optional): 模块实现类型. Defaults to None.

        Raises:
            error.ModuleLoadError: 模块不支持或模块未实现
        """
        info = cell.info

        # 如果当前实现类型是基本类型，则只有一种实现类型，不需要校验
        # if info.kind == BASIC:
        #     continue

        # 验证当前实现是否存咋支持的 kinds 中
        if kind not in info.kinds:
            raise error.ModuleLoadError(
                f"the kind '{kind}' is not supported in {info.name}"
            )

    def log(self, log: ModuleLog):
        # TODO: 发送日志后的处理函数

        if self.__log_callback is not None:
            self.__log_callback(log)

    # ----- 模块控制 ----- #

    # 启动模块单元
    def start(self, name: str, with_sub: bool = True, with_sup: bool = False):
        """启动模块。
        注意递归启动有方向性，递归父模块时只会递归启动父模块，子模块同理

        Args:
            name (str): 模块名称
            with_sub (bool, optional): 是否递归启动父模块. Defaults to True.
            with_sup (bool, optional): 是否递归启动父模块. Defaults to False.

        Raises:
            FileNotFoundError: _description_
            e: _description_

        Returns:
            Tuple[bool, ModuleStatus]: 是否运行成功，当前的状态（运行成功为None）
        """

        cell = self._cell(name, force=True)

        try:
            # 0. 如果当前模块状态不是在停止状态 则不能停止
            cur_status = cell.status
            if cur_status != ModuleStatus.Stopped:
                return False, cur_status

            # 1. 首先启动启动子模块
            module = cell.module
            module.before_starting_submodules()
            self._update_status(cell, ModuleStatus.Starting)

            if with_sub:
                for sub_name, sub_cell in cell.sub.items():
                    if sub_cell.is_null:
                        continue

                    self.start(sub_name, with_sub=True, with_sup=False)

            # 2. 更新配置信息
            try:
                module.load_config()
            except KeyError:
                raise error.ModuleRuntimeError(
                    f"configuration about module '{module.name}' is missing"
                )

            # TODO: 在配置信息更新之后，启动子模块对应的线程

            # 3. 模块的自定义启动逻辑
            module.handle_starting()

            # 4. 模块自检
            try:
                module.check()
            except BaseException as e:
                raise error.ModuleCheckError(name, e)

            # 5. 钩子函数
            self._update_status(cell, ModuleStatus.Started)

            if with_sup and cell.sup is not None:
                self.start(cell.sup.name, with_sub=False, with_sup=True)

        except error.ModuleError as e:
            # 如果模块启动曹组
            self._update_status(cell, ModuleStatus.StartError)
            self.stop(name)
            raise e

    # 停止模块单元
    def stop(self, name: str):
        """停止模块

        Args:
            name (str): 模块名称

        Returns:
            bool: 是否运行成功，当前的状态（运行成功为None）
        """

        cell = self._cell(name)

        # 运行成功之后可以停止, 发生异常需要级联停止
        if not (
            cell.status == ModuleStatus.Started or ModuleStatus.is_error(cell.status)
        ):
            return

        module = cell.module

        # 1. 先设置标志位
        module.handle_stopping()
        self._update_status(cell, ModuleStatus.Stopping)

        # 2. 关闭内部的线程处理
        module.wait_threads()

        # 3. 关闭子线程
        for sub_name, sub_cell in cell.sub.items():
            if sub_cell.is_null:
                continue
            self.stop(sub_name)

        module.after_stopping_submodules()
        self._update_status(cell, ModuleStatus.Stopped)

    def send(self, msg: Message):
        if self.__booter_cell is None:
            return

        # 只能通过 booter 进行交互
        booter: BooterInterface = self.__booter_cell.module
        booter.send(msg)

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

        cell = self._cell(name, force=True)

        # 判断模块状态是否可切换
        cur_status = cell.status
        if not ModuleStatus.can_change(cur_status):
            return False, cur_status

        # 验证类型是否满足条件
        self._check_kind_exist(cell, kind)
        # 模块不限定 basic 只存在一种实现类型，其只作为最基本的实现类型
        # elif kind == BASIC:
        #     if len(info.kinds) != 0:
        #         raise ValueError(f"the module '{name}' is not single implementation")
        #     return

        # 判断模块是否存在
        if kind == NULL:
            # 如果置空，则需要清空记录
            cell.module = None
            self._update_status(cell, ModuleStatus.NotLoaded)
        else:
            # 1. 使用动态导入模块
            module: BasicModule = self.__dynamic_import_module(name, kind)()
            # 2. 设置模块
            cell.module = module
            # 3. 依赖注入
            cell.inject(self.log)
            # 4. 修改状态
            self._update_status(cell, ModuleStatus.Stopped)

        cell.info.kind = kind

        # 2. 重新设置父模块中的指针
        if cell.sup is not None:
            sup_cell = cell.sup

            # 更新父 Cell 的子 Cell 指针
            sup_cell.sub[name] = cell

            # 更新父模块的子模块
            print(sup_cell.module.name)
            sup_cell.module.update_sub_module(cell.module)

        # FIXME: 使用抛出异常解决运行不成功的问题
        return True, None

    # ----- Getter ----- #

    def info(self, name: str) -> ModuleInfo | None:
        cell = self.__module_cells.get(name, None)

        return cell.info if cell is not None else None

    def module(self, name: str) -> BasicModule | None:
        cell = self.__module_cells.get(name, None)

        return cell.module if cell is not None else None

    def _cell(self, name: str, force: bool = True) -> ModuleManageCell:
        cell = self.__module_cells.get(name)

        if cell is None and force:
            raise error.ModuleRuntimeError(f"module '{name}' not found")

        return cell

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

    # ----- Setter ----- #

    def _update_status(self, cell: ModuleManageCell, new_status: ModuleStatus):
        name = cell.info.name

        # Notice: 必须使用该函数进行更新状态
        cell.status = new_status
        if cell.module is not None:
            cell.module.update_status(new_status)
        self.log(ModuleStatusLog(name, new_status))

    def set_log_callback(self, callback: LogCallBack):
        self.__log_callback = callback


# Notice: 使用单例模式使用模块管理器
def init_manager() -> ModuleManager:
    try:
        manager = ModuleManager()
    except error.ModuleLoadError as e:
        # 首次加载模块失败则会停止
        print(e.args[0])
        sys.exit()

    return manager


MANAGER = init_manager()
