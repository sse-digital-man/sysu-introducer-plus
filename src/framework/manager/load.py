from typing import Dict, List, Tuple, Any

from utils.file import load_yaml, save_json

from ..config import load_config, ModuleConfig
from ..info import ModuleInfo, ModuleDescriptor, to_instance_label

from .utils import BASIC, select_supported_kinds
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
            descriptor = ModuleDescriptor.new_except(name, kinds)
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


def _load_module(path: str) -> Tuple[Dict[str, ModuleInfo], str]:
    raw_modules_info: Dict[str, Dict] = load_yaml(path)

    modules_info: Dict[str, ModuleInfo] = {}
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
SYSTEM_PATH = "conf/system.json"
USER_PATH = "conf/user.json"
USER_FORMAT_PATH = "conf/user_format.json"

MODULES_PATH = "conf/modules.yaml"


class ModuleLoader:
    def __init__(self):
        # 根管理单元
        self.__root_cell: ModuleManageCell = None

        # 模块管理单元池
        # Notice: 不需要使用单独记录模块管理单元的引用次数
        # ModuleManageCell.sup 可以记录引用次数
        self.__cell_pool: Dict[str, ModuleManageCell] = {}

        # User 配置文件的原始数据在此处维护
        self.__raw_user_config: Dict[str, Dict[str, Dict[str, Any]]] = {}

    # 创建模块管理单元
    def __create_module_cells(
        self, modules_info: Dict[str, ModuleInfo], name: str, kind: str
    ) -> ModuleManageCell:

        info = modules_info[name]
        cell = ModuleManageCell(info, kind)
        self.__cell_pool[to_instance_label(name, kind)] = cell

        # 获取 子模块描述符 列表
        sub_descriptors = info.sub_descriptors
        instance_descriptors = info.instance_sub_descriptors(kind)
        if instance_descriptors is not None:
            sub_descriptors.update(instance_descriptors)

        for sub_name, sub_descriptor in sub_descriptors.items():
            sub_info = modules_info[sub_name]

            # 根据模块描述符，筛选支持的实现
            sub_kinds = select_supported_kinds(sub_info, sub_descriptor)
            if len(sub_kinds) == 0:
                raise ValueError("not kind can't be supported")

            sub_kind = sub_info.default
            if sub_kind not in sub_kinds:
                sub_kind = sub_kinds[0]

            # 如果 cell 不存在则创建，存在则直接使用 dp 思想
            pool_name = to_instance_label(sub_name, sub_kind)
            sub_cell = self.__cell_pool.get(pool_name, None)
            if sub_cell is None:
                sub_cell = self.__create_module_cells(modules_info, sub_name, sub_kind)

            # 在父模块中添加子模块
            cell.set_sub(sub_name, sub_cell)
            # 在子模块中添加父模块
            sub_cell.set_sup(name, cell)

        return cell

    def load(self):
        # 1. 导入基础模块信息
        modules_info, root_name = _load_module(MODULES_PATH)

        # 2. 通过树状关系创建模块管理单元，并且填充 cell 池
        root_cell = self.__create_module_cells(modules_info, root_name, BASIC)

        # 3. 读取模块的配置信息
        system_config, raw_user_config, user_format = load_config(
            SYSTEM_PATH, USER_PATH, USER_FORMAT_PATH
        )

        for cell in self.__cell_pool.values():
            # Notice: cell_poll 中 key 值为 instance_label
            name = cell.name
            module_config = ModuleConfig(
                system_config.get(name, {}),
                user_format.get(name, {}),
            )

            cell.set_config(module_config)
            cell.inject()

        # 4. 赋值
        self.__root_cell = root_cell
        self.__raw_user_config = raw_user_config

    def save_instance_config(self, name: str, kind: str, content: Dict[str, Any]):
        for field, value in content.items():
            self.__raw_user_config[name][kind][field] = value

        save_json(USER_PATH, self.__raw_user_config)

    @property
    def root_cell(self) -> ModuleManageCell:
        return self.__root_cell

    @property
    def cell_pool(self) -> Dict[str, ModuleManageCell]:
        return self.__cell_pool
