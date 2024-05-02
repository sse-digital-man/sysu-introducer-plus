from typing import List

class ModuleInfo:
    def __init__(self, name: str, alias: str, 
                kind: str="basic", path: str="", modules: List[str]=[]):
        self.__name = name
        self.__alias = alias
        self.__kind = kind
        
        self.__path = path
        self.__modules = modules

        self.__object = None

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
    def object(self) -> str:
        return self.__object
    
    