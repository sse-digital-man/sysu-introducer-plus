from typing import List, Self
from enum import IntEnum, unique


@unique
class ModuleStatus(IntEnum):
    NotLoaded = 0
    Stopped = 1
    Starting = 2
    Started = 3
    Stopping = 4

    def can_change(self: Self) -> bool:
        return self in [ModuleStatus.NotLoaded, ModuleStatus.Stopped]


moduleStatusMap = {
    ModuleStatus.NotLoaded: "未加载",
    ModuleStatus.Stopped: "未运行",
    ModuleStatus.Starting: "启动中",
    ModuleStatus.Started: "运行中",
    ModuleStatus.Stopping: "停止中",
}


class ModuleInfo:
    def __init__(
        self,
        name: str,
        alias: str,
        kinds: List[str],
        kind: str,
        not_null: bool,
        path: str,
        submodules: List[str],
    ):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        self.__kinds: List[str] = kinds
        self.__not_null = not_null
        self.__path = path

        # Notice: 当这个模块支持空时 则需要添加空值类型
        if len(kinds) == 0 and kind == "basic":
            self.__kinds.append("basic")

        if not not_null:
            self.__kinds.insert(0, "null")

        # 记录父子模块的关系 (只存储模块名, 不存储对象)
        self.__sup: str = None
        self.__sub: List[str] = submodules
        self.__depth = -1

        # 运行状态信息 (运行阶段的状态, 不再此处存储)
        # self.__status: ModuleStatus = ModuleStatus.NotLoaded

    def to_dict(self):
        return {
            "alias": self.alias,
            "name": self.name,
            "kind": self.kind,
            "kinds": self.kinds,
            "modules": self.sub,
        }

    # ---- Getter ------ #

    @property
    def name(self) -> str:
        return self.__name

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def kind(self) -> str:
        """返回当前实现类型"""
        return self.__kind

    @property
    def kinds(self) -> List[str]:
        """返回支持的实现类型列表"""
        return self.__kinds

    @property
    def not_null(self) -> bool:
        return self.__not_null

    @property
    def path(self) -> str:
        return self.__path

    @property
    def sup(self) -> str:
        return self.__sup

    @property
    def sub(self) -> List[str]:
        return self.__sub

    @property
    def depth(self) -> int:
        return self.__depth

    # ---- Setter ------ #

    @kind.setter
    def kind(self, kind: str):
        self.__kind = kind

    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @sup.setter
    def sup(self, name: str):
        self.__sup = name
