from typing import List, Dict

from utils import error

from .utils import dynamic_import_module
from ..info import ModuleInfo, ModuleDescriptor


def _check_module_sub(module_info: Dict[str, ModuleInfo]) -> str:
    # 验证所有子模块是否存在, 并加载子模块的嵌套深度
    in_degree = dict.fromkeys(module_info.keys(), 0)

    def __check_submodule_exist(submodules: List[str]):
        for submodule in submodules:
            sub_info = module_info.get(submodule, None)
            if sub_info is None:
                raise FileNotFoundError(f"{submodule} in {info.name} not found")

            in_degree[submodule] = in_degree.get(submodule) + 1

    for info in module_info.values():
        __check_submodule_exist(info.sub)

        for kind in info.kinds:
            __check_submodule_exist(info.instance_sub_descriptors(kind).keys())

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

    # 验证所支持的模块是否实现
    for info in module_info.values():
        for kind in info.kinds:
            dynamic_import_module(info, kind)

    return root_name


def _check_module_kind(module_info: Dict[str, ModuleInfo]):
    def __check_submodules_descriptors(submodules: Dict[str, ModuleDescriptor]):
        for submodule, descriptor in submodules.items():
            for cond_kind in descriptor.cond_kinds:
                if cond_kind in module_info[submodule].kinds:
                    continue

                raise FileNotFoundError(
                    f"'{cond_kind}' as the condition for the module '{submodule}'"
                    + "is not found in '{info.name}'"
                )

    for info in module_info.values():
        if info.default not in info.kinds:
            raise FileNotFoundError(
                f"default kind '{info.default}' not found in module '{info.name}'"
            )

        # 验证子模块的模块描述符中的 实现类型 是否存在
        __check_submodules_descriptors(info.sub_descriptors)

        # 验证实现类型的 子模块中的模块描述符中的 实现类型是否存在
        for kind in info.kinds:
            __check_submodules_descriptors(info.instance_sub_descriptors(kind))


# 验证模块信息
def check_module(module_info: Dict[str, ModuleInfo]) -> str:

    # 从 实现类型 角度进行验证
    # 1. 默认实现类型
    # 2. 子模块的 实现类型 条件
    # 3. 实现实例中 子模块的 实现类型 条件是否存在
    _check_module_kind(module_info)

    # 从 子模块 角度进行验证
    root_name = _check_module_sub(module_info)

    return root_name
