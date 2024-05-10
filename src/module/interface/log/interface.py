from abc import ABCMeta
from typing import Dict
from enum import IntEnum

import json

class ModuleLogKind(IntEnum):
    # 模块状态相关
    ModuleStatus = 1

    # 消息发送相关
    Message = 2

class ModuleLog(metaclass=ABCMeta):
    def __init__(self, kind: ModuleLogKind, content: Dict):
        self.kind = kind
        self.content = content

    def to_json(self) -> str:
        data = {
            "kind": self.kind,
            "content": self.content
        }

        return json.dumps(data)