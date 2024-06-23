from typing import List, Dict, Self
from enum import Enum, IntEnum, unique


def to_instance_label(name: str, kind: str):
    return f"{name}_{kind}"


@unique
class ModuleStatus(IntEnum):
    NotLoaded = 0
    Stopped = 1
    Starting = 2
    Started = 3
    Stopping = 4

    # 发生异常，模块发生异常，就相当于
    StartError = 5
    RunError = 6
    StopError = 7

    def can_change(self: Self) -> bool:
        """当模块处于运行中、启动中和停止中时，模块是羡慕类型不能被切换

        Returns:
            bool: 能否被切换
        """
        return self in [
            ModuleStatus.NotLoaded,
            ModuleStatus.Stopped,
        ]

    def is_error(self: Self) -> bool:
        return self in [
            ModuleStatus.StartError,
            ModuleStatus.RunError,
            ModuleStatus.StopError,
        ]


moduleStatusMap = {
    ModuleStatus.NotLoaded: "未加载",
    ModuleStatus.Stopped: "未运行",
    ModuleStatus.Starting: "启动中",
    ModuleStatus.Started: "运行中",
    ModuleStatus.Stopping: "停止中",
    ModuleStatus.StartError: "启动异常",
    ModuleStatus.RunError: "运行异常",
    ModuleStatus.StopError: "停止异常",
}


class ModuleName(Enum):
    BOOTER = "booter"
    CORE = "core"
    BOT = "bot"
    CALLER = "caller"
    SEARCHER = "searcher"
    SPEAKER = "speaker"
    CRAWLER = "crawler"
    RENDERER = "renderer"


class ModuleDescriptorKind(Enum):
    ALL = 0
    SOME = 1
    EXPECT = 2


class ModuleDescriptor:
    def __init__(
        self,
        name: str,
        kind: ModuleDescriptorKind,
        cond_kinds: List[str],
    ):
        self.__name = name
        self.__kind = kind
        self.__cond_kinds = cond_kinds

    @staticmethod
    def new_all(name: str):
        return ModuleDescriptor(name, ModuleDescriptorKind.ALL, [])

    @staticmethod
    def new_some(name: str, kinds: List[str]):
        return ModuleDescriptor(name, ModuleDescriptorKind.SOME, kinds)

    @staticmethod
    def new_except(name: str, kinds: List[str]):
        return ModuleDescriptor(name, ModuleDescriptorKind.EXPECT, kinds)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def kind(self) -> ModuleDescriptorKind:
        return self.__kind

    @property
    def cond_kinds(self) -> List[str]:
        return self.__cond_kinds


class ModuleInfo:

    def __init__(
        self,
        name: str,
        alias: str,
        path: str,
        submodules: Dict[str, ModuleDescriptor],
        kinds: Dict[str, Dict[str, ModuleDescriptor]],
        default: str,
        not_null: bool,
    ):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__path = path

        # 记录父子模块的关系 (只存储模块名, 不存储对象)
        self.__sup: str = None
        self.__sub: Dict[str, ModuleDescriptor] = submodules
        self.__depth = -1

        self.__kinds: Dict[str, Dict[str, ModuleDescriptor]] = kinds
        self.__default: str = default
        self.__not_null = not_null

        # 运行状态信息 (运行阶段的状态, 不再此处存储)
        # self.__status: ModuleStatus = ModuleStatus.NotLoaded

    # ---- Getter ------ #

    @property
    def name(self) -> str:
        return self.__name

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def default(self) -> str:
        return self.__default

    @property
    def kinds(self) -> List[str]:
        """返回支持的实现类型列表"""
        return list(self.__kinds.keys())

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
        return list(self.__sub.keys())

    @property
    def sub_descriptors(self) -> Dict[str, ModuleDescriptor]:
        return self.__sub

    @property
    def depth(self) -> int:
        return self.__depth

    def instance_sub_descriptors(self, kind: str) -> Dict[str, ModuleDescriptor] | None:
        return self.__kinds.get(kind, None)

    # ---- Setter ------ #

    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @sup.setter
    def sup(self, name: str):
        self.__sup = name
