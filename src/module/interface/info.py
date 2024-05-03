from typing import List

class ModuleInfo:
    def __init__(self, name: str, alias: str, 
                kind: str="basic", path: str="", modules: List[str]=[]):
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        
        self.__path = path
        self.__modules = modules

        self.__depth = -1;

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

    ''' ---- Setter ------ '''
    
    @depth.setter
    def depth(self, depth: int):
        self.__depth = depth