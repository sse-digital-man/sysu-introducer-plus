from typing import Dict, List, Tuple, Any

from utils.file import load_yaml, save_json

from ..config import load_config, ModuleConfig
from ..info import ModuleInfo, ModuleDescriptor

from .cell import ModuleManageCell
from .check import check_module


def _convert_module_descriptor(raw_descriptor: str) -> Tuple[str, ModuleDescriptor]:
    parts = raw_descriptor.replace(" ", "").split(":")
    name, expr = parts[0], parts[1]

    if len(parts) == 1 or expr == "*":
        descriptor = ModuleDescriptor.new_all(name)

    elif expr.startswith("[") or expr.startswith("!["):
        if expr[-1] != "]":
            raise ValueError(f"expr '{expr}' in module'{name}' is invalid")

        if expr.startswith("["):
            kinds = expr[1:-1].split(",")
            descriptor = ModuleDescriptor.new_some(name, kinds)
        else:
            kinds = expr[2:-1].split(",")
            descriptor = ModuleDescriptor.new_some(name, kinds)
    else:
        descriptor = ModuleDescriptor.new_some(name, [expr])

    return name, descriptor


def _convert_module_descriptors(
    descriptor_list: List[str],
) -> Dict[str, ModuleDescriptor]:
    descriptors = {}
    for raw_descriptor in descriptor_list:
        name, descriptor = _convert_module_descriptor(raw_descriptor)
        descriptors[name] = descriptor

    return descriptors


def _load_module(path: str):
    raw_modules_info: Dict[str, Dict] = load_yaml(path)

    modules_info: Dict[str, Dict] = {}
    for name, module in raw_modules_info.items():
        default_kind = module.get("default", "basic")
        not_null = module.get("notNull", True)

        # 1. 加载子模块
        submodules = _convert_module_descriptors(module.get("modules", []))

        # 2. 加载实现类型
        raw_kinds: List[str] = module.get("kinds", [])

        if len(raw_kinds) == 0 and default_kind == "basic":
            raw_kinds.append("basic")
        if not not_null:
            raw_kinds.append("null")

        kinds = {}
        for instance in raw_kinds:
            if isinstance(instance, str):
                kinds[instance] = {}
            else:
                kinds[instance["kind"]] = _convert_module_descriptors(
                    instance.get("modules", [])
                )

        # 3. 创建模块信息对象
        modules_info[name] = ModuleInfo(
            name,
            module["alias"],
            module.get("path", ""),
            submodules,
            kinds,
            default_kind,
            not_null,
        )

    root_name = check_module(modules_info)

    return modules_info, root_name


ConfigType = Dict[str, Dict[str, Dict[str, Any]]]


# 配置文件路径
SYSTEM_PATH = "system.json"
USER_PATH = "user.json"
USER_FORMAT_PATH = "user_format.json"

MODULES_PATH = "conf/modules.yaml"


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
