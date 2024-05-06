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
    

class ModuleInfo:
    def __init__(self, name: str, alias: str, 
                kind: str="basic", path: str="", modules: List[str]=[]):
        # 基本信息
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        self.__path = path

        # 子模块信息
        self.__modules = modules
        self.__depth = -1

        # 运行状态信息
        self.__status: ModuleStatus = ModuleStatus.NotLoaded 

    ''' ---- Getter ------ '''
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def kind(self) -> str:
        return self.__kind

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
    
    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth

    @status.setter
    def status(self, status: ModuleStatus):
        self.__status = status