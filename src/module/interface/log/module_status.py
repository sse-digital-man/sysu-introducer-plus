from .interface import ModuleLog, ModuleLogKind
from ..info import ModuleStatus

class ModuleStatusLog(ModuleLog):
    def __init__(self, name: str, status: ModuleStatus):
        super().__init__(ModuleLogKind.ModuleStatus)

        self.name = name
        self.status = status