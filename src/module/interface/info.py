from typing import List
from enum import Enum, IntEnum, unique

class ModuleName(Enum):
    Booter = "booter"
    Core = "core"
    Bot = "bot"
    Caller = "caller"
    Searcher = "searcher"
    Crawler = "crawler"

@unique
class ModuleStatus(IntEnum):
    NotLoaded = 0
    Stopped = 1
    Starting = 2
    Started = 3
    Stopping = 4

moduleStatusMap = {
    ModuleStatus.NotLoaded: "未加载",
    ModuleStatus.Stopped: "未运行",
    ModuleStatus.Starting: "启动中",
    ModuleStatus.Started: "运行中",
    ModuleStatus.Stopping: "停止中",
}


class ModuleInfo:
    def __init__(self, name: str, alias: str, kinds: List[str]=[],
                kind: str="basic", path: str="", modules: List[str]=[]):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        self.__path = path
        self.__kinds = kinds

        # 子模块信息
        self.__modules = modules
        self.__depth = -1

        # 运行状态信息
        self.__status: ModuleStatus = ModuleStatus.NotLoaded 

    def to_dict(self):
        return {
            "alias": self.alias,
            "name": self.name,
            "kind": self.kind,
            "kinds": self.kinds,
            "status": self.status,
            "modules": self.modules
        }        

    ''' ---- Getter ------ '''
    
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
    def path(self) -> str:
        return self.__path

    @property
    def modules(self) -> List[str]:
        return self.__modules
    
    @property
    def depth(self) -> int:
        return self.__depth
    
    @property
    def status(self) -> ModuleStatus:
        return self.__status

    ''' ---- Setter ------ '''

    @kind.setter
    def kind(self, kind: str):
        self.__kind = kind

    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @status.setter
    def status(self, status: ModuleStatus):
        self.__status = status