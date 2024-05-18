from abc import ABCMeta
from typing import Dict, Callable
from enum import IntEnum

import json

from utils.time import now_str


class ModuleLogKind(IntEnum):
    # 模块状态相关
    STATUS = 1

    # 消息发送相关
    MESSAGE = 2

    # 消息处理相关
    HANDLE = 3


class ModuleLog(metaclass=ABCMeta):
    def __init__(
        self,
        log_kind: ModuleLogKind,
        content: Dict,
        name: str = None,
        kind: str = None,
    ):
        self.log_kind = log_kind
        self.content = content
        self.name = name
        self.kind = kind
        self.time = now_str()

    def to_json(self) -> str:
        data = {"logKind": self.log_kind, "content": self.content, "time": self.time}

        if self.name is not None:
            data["name"] = self.name
        if self.kind is not None:
            data["kind"] = self.kind

        return json.dumps(data)


ModuleCallback = Callable[[ModuleLog], None]
