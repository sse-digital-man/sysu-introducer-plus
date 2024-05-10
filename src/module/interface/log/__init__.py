from enum import IntEnum

from message import MessageKind, Message
from .interface import ModuleLog, ModuleLogKind
from ..info import ModuleStatus

class ModuleStatusLog(ModuleLog):
    def __init__(self, name: str, status: ModuleStatus):
        super().__init__(ModuleLogKind.ModuleStatus, {
            "name": name,
            "status": status,
        })

class MessageLog(ModuleLog):
    def __init__(self,messageKind: MessageKind, content: str, to_admin: bool=False):
        super().__init__(ModuleLogKind.Message, {
            "content": content,
            "kind": messageKind,
            "toAdmin": to_admin,
        })
    
    @staticmethod
    def from_message(message: Message, to_admin: bool=False):
        return MessageLog(message.kind, message.content, to_admin)