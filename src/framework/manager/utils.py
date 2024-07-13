from importlib import import_module
from typing import List
from utils import error

from ..info import ModuleInfo, ModuleDescriptor, ModuleDescriptorKind

NULL = "null"
BASIC = "basic"


# 动态导入模块
def dynamic_import_module(info: ModuleInfo, kind: str):
    # 生成对应的类的名称
    # 如果类型是全大写，说明是缩写情况，否则只大写开头字母
    def generate_name(name: str, kind: str):
        if kind is None:
            kind = "basic"
        elif not kind.isupper():
            kind = kind.title()
        else:
            kind = kind[0].upper() + kind[1:]

        return kind + name.title()

    if kind == NULL:
        return None

    # 收集包路径
    names: List[str] = ["module"]

    if len(info.path) != 0:
        names.append(info.path)
    names.append(info.name)

    # 路径只能包含小写字母
    if kind != BASIC:
        names.append(kind.lower())

    try:
        class_name = generate_name(info.name, kind)
        return getattr(import_module(".".join(names)), class_name)
    except ModuleNotFoundError as e:
        path = str(e.name)

        # 当导入 module 模块时发生错误，则说明未实现
        if path.startswith("module"):

            raise error.ModuleLoadError(
                f"the kind '{kind}' in '{info.name}' is not implemented or imported error"
            )

        raise e


def select_supported_kinds(info: ModuleInfo, descriptor: ModuleDescriptor) -> List[str]:
    """根据模块描述符选择，该模块支持的模块类型列表

    Args:
        info (ModuleInfo): 模块信息
        descriptor (ModuleDescriptor): 模块描述符

    Returns:
        str: 支持的模块类型列表
    """
    descriptor_kind = descriptor.kind
    if descriptor_kind is ModuleDescriptorKind.ALL:
        return info.kinds

    cond_kinds = descriptor.cond_kinds
    if descriptor_kind is ModuleDescriptorKind.SOME:
        return cond_kinds

    if descriptor_kind is ModuleDescriptorKind.EXPECT:
        rest_kinds = set(info.kinds)
        for cond_kind in cond_kinds:
            rest_kinds.remove(cond_kind)

        return rest_kinds

    return []
