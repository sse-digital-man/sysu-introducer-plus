from enum import IntEnum

class MessageKind(IntEnum):
    Watcher = 0
    Admin = 1
    Signal = 2

class Message:
    def __init__(self, kind: MessageKind, content: str):
        self.kind = kind

        # 这里的内容既可以用户/管理员的消息，也可以存储信号类型
        self.content = content
