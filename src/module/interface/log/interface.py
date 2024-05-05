from abc import ABCMeta
from enum import IntEnum

import json

class ModuleLogKind(IntEnum):
    # 模块状态相关
    ModuleStatus = 1

    # 消息发送相关
    Message = 2

class ModuleLog(metaclass=ABCMeta):
    def __init__(self, kind: ModuleLogKind):
        self.kind = kind

    def to_json(self) -> str:
        json_object = {}

        for (key, value) in vars(self).items():
            json_object[key] = value

        return json.dumps(json_object)