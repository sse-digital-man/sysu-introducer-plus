from typing import List, Dict, Any, Self
from enum import Enum, IntEnum, unique


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


class ModuleInfo:
    def __init__(
        self,
        name: str,
        alias: str,
        default: str,
        kinds: List[str],
        not_null: bool,
        path: str,
        submodules: List[str],
    ):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__kinds: List[str] = kinds
        self.__default: str = default
        self.__not_null = not_null
        self.__path = path

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
    def default(self) -> str:
        return self.__default

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

    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @sup.setter
    def sup(self, name: str):
        self.__sup = name


class ModuleDockerInfo:
    class Port:
        def __init__(self, in_port: int, out_port: int, protocol: str = "tcp"):
            self.in_port = in_port
            self.out_port = out_port
            self.protocol = protocol

    def __init__(
        self, tag: str, envs: Dict[str, str], ports: Dict[str, Port], is_daemon: bool
    ):
        self.tag = tag
        self.envs = envs
        self.ports = ports
        self.is_daemon = is_daemon

    def out_port(self, field: str):
        return self.ports[field].out_port

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> Self:
        format_ports = {}
        for field, content in format_ports.items():
            if isinstance(content, int):
                port = ModuleDockerInfo.Port(content, content)
            elif isinstance(content, dict):
                in_port = content["in"]
                port = ModuleDockerInfo.Port(
                    in_port, content.get("out", in_port), content.get("protocol", "tcp")
                )
            else:
                raise ValueError("docker config info error")

            format_ports[field] = port

        return ModuleDockerInfo(d["tag"], d["envs"], format_ports, d["isDaemon"])
