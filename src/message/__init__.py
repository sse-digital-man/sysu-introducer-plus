from enum import IntEnum
from datetime import datetime

class MessageKind(IntEnum):
    Watcher = 0
    Admin = 1
    Command = 2
    Assistant = 3


message_kind_map = {0: "观众", 1: "管理员", 2: "指令", 3: "数字人"}


class Message:
    def __init__(self, kind: MessageKind, content: str):
        self.kind = kind
        # 这里的内容既可以用户/管理员的消息，也可以存储信号类型
        self.content = content
        self.sim = 0
        self.timestamp = datetime.now().timestamp()

    def __repr__(self) -> str:
        label = message_kind_map[self.kind]
        return f"[{label}]{self.content}"
