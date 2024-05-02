from typing import Dict

from utils.file import load_json
from .info import ModuleInfo


CONFIG_PATH = "src/modules.json"

class ModuleContainer:
    def __init__(self):
        self.__module_info_list: Dict[str, ModuleInfo] = {}

        self.__load_modules()

        print(self.__show_as_table())
        exit()
        

    def __load_modules(self):
        modules_info: Dict[str, Dict] = load_json(CONFIG_PATH)

        for (name, content) in modules_info.items():
            self.__module_info_list[name] = \
                ModuleInfo(name, content["alias"], 
                    content.get("default", "basic"),
                    content.get("path", ""),
                    content.get("modules", [])
                )
            

    def __show_as_table(self) -> str:
        from tabulate import tabulate

        header = ["name", "alias", "kind", "path", "modules"]
        
        rows = [
            [info.name, info.alias, info.kind, info.path, ", ".join(info.modules)] 
            for info in self.__module_info_list.values()
        ]

        return tabulate(rows, header, tablefmt="github")

        