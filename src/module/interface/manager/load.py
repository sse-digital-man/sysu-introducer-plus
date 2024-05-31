from typing import Dict, List, Any
from utils import error
from utils.file import load_json, save_json

from ..config import load_config, ModuleConfig
from ..info import ModuleInfo

from .cell import ModuleManageCell
from .utils import dynamic_import_module


def _load_module(path: str):
    # 1. 从配置文件中加载模块信息
    raw_modules_info: Dict[str, Dict] = load_json(path)

    modules_info: Dict[str, Dict] = {}
    for name, content in raw_modules_info.items():
        kinds: List[str] = content.get("kinds", [])
        default_kind = content.get("default", "basic")

        # 转换语法糖
        if len(kinds) == 0 and default_kind == "basic":
            kinds.append("basic")

        info = ModuleInfo(
            name,
            content["alias"],
            default_kind,
            kinds,
            content.get("notNull", True),
            content.get("path", ""),
            content.get("modules", []),
        )

        modules_info[name] = info

    # 2. 验证模块情况, 并返回根节点
    root_name = _check_module(modules_info)

    return modules_info, root_name


def _check_module(module_info: Dict[str, ModuleInfo]) -> str:
    # 验证所有子模块是否存在, 并加载子模块的嵌套深度
    in_degree = dict.fromkeys(module_info.keys(), 0)

    for info in module_info.values():
        for submodule in info.sub:
            sub_info = module_info.get(submodule, None)
            if sub_info is None:
                raise FileNotFoundError(f"{submodule} in {info.name} not found")

            in_degree[submodule] = in_degree.get(submodule) + 1

            # 设置 ModuleInfo 中子节点指向父节点的指针
            sub_info.sup = info.name

    # 存储添加入度为0的模块
    queue = list(filter(lambda name: in_degree[name] == 0, module_info.keys()))

    # 如果没有入度为 0 的节点，说明存在循环依赖
    if len(queue) == 0:
        raise error.ModuleLoadError("circular dependency between modules")
    # 出现多个booter
    if len(queue) != 1:
        raise error.ModuleLoadError("multiple root module are loaded")

    root_name = queue[0]

    # 使用 BFS 计算所有节点深度
    depth = 0
    while len(queue) > 0:
        size = len(queue)

        for _ in range(size):
            name = queue.pop(0)
            info = module_info[name]
            info.depth = depth

            for submodule in info.sub:
                in_degree[submodule] -= 1

                if in_degree[submodule] == 0:
                    queue.append(submodule)

        depth += 1

    # 验证模块实现实例
    for info in module_info.values():
        # 验证所支持的模块是否实现
        for kind in info.kinds:
            dynamic_import_module(info, kind)

    return root_name


ConfigType = Dict[str, Dict[str, Dict[str, Any]]]


# 配置文件路径
SYSTEM_PATH = "system.json"
USER_PATH = "user.json"
USER_FORMAT_PATH = "user_format.json"

MODULES_PATH = "modules.json"


class ModuleLoader:
    def __init__(self):
        self.__module_cells: Dict[str, ModuleManageCell] = {}
        self.__booter_cell: ModuleManageCell = None

        # User 配置文件的原始数据在此处维护
        self.__raw_user_config: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def load(self):
        # 1. 导入基础模块信息
        modules_info, root_name = _load_module(MODULES_PATH)

        # 2. 创建模块管理单元
        module_cells: Dict[str, ModuleManageCell] = {
            name: ModuleManageCell(info) for name, info in modules_info.items()
        }

        # 3. 设置父子模块管理单元指针,
        for name, cell in module_cells.items():
            # 遍历加载所有子模块
            for submodule in cell.info.sub:
                # 在父模块中添加子模块
                cell.set_sub(submodule, module_cells[submodule])
                # 在子模块中添加父模块
                module_cells[submodule].set_sup(cell)

        # 4. 设置 模块配置信息
        system_config, raw_user_config, user_format = load_config(
            SYSTEM_PATH, USER_PATH, USER_FORMAT_PATH
        )
        for name, module_cell in module_cells.items():
            module_cell.set_config(
                ModuleConfig(
                    system_config.get(name, {}),
                    user_format.get(name, {}),
                )
            )

        # 5. 设置 docker 配置信息（将 Docker 配置担负划分出来）

        # 6. 最后手动注入依赖信息
        for cell in module_cells.values():
            cell.inject()

        self.__module_cells = module_cells
        self.__booter_cell = module_cells[root_name]
        self.__raw_user_config = raw_user_config

    def save_instance_config(self, name: str, kind: str, content: Dict[str, Any]):
        for field, value in content.items():
            self.__raw_user_config[name][kind][field] = value

        save_json(USER_PATH, self.__raw_user_config)

    @property
    def module_cells(self):
        return self.__module_cells

    @property
    def booter_cell(self):
        return self.__booter_cell
