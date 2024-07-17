from message import MessageKind, Message
from framework.info import ModuleStatus, ModuleName

from .interface import ModuleLog, ModuleLogKind
from .logger import Logger

LOGGER = Logger()


class StatusLog(ModuleLog):
    def __init__(self, name: str, kind: str, status: ModuleStatus):
        super().__init__(
            ModuleLogKind.STATUS,
            {
                "status": status,
            },
            name=name,
            kind=kind,
        )


class MessageLog(ModuleLog):
    def __init__(self, messageKind: MessageKind, content: str, to_admin: bool = False):
        data = {
            "content": content,
            "kind": messageKind,
        }

        if to_admin:
            data["toAdmin"] = True

        super().__init__(
            ModuleLogKind.MESSAGE,
            data,
            name=ModuleName.CORE.value,
        )

    @staticmethod
    def from_message(message: Message, to_admin: bool = False):
        return MessageLog(message.kind, message.content, to_admin)


class HandleLog(ModuleLog):
    def __init__(self, name: str, kind: str, time: float):
        super().__init__(ModuleLogKind.HANDLE, {"time": time}, name=name, kind=kind)
