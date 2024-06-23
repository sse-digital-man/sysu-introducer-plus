from importlib import import_module
from typing import List
from utils import error

from ..info import ModuleInfo

NULL = "null"
BASIC = "basic"


# 动态导入模块
def dynamic_import_module(info: ModuleInfo, kind: str):
    # 生成对应的类的名称
    def generate_name(name: str, kind: str):
        if kind is None:
            kind = "basic"

        return kind.title() + name.title()

    if kind == NULL:
        return None

    # 收集包路径
    names: List[str] = ["module"]

    if len(info.path) != 0:
        names.append(info.path)
    names.append(info.name)

    # 如果传输进来的实现类型为空，则读取 kind
    if kind != BASIC:
        names.append(kind)

    try:
        class_name = generate_name(info.name, kind)
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
