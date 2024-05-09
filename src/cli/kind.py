from enum import Enum

class UnknownCommandError(BaseException):
    def __init__(self):
        super().__init__("unknown command")


class CommandKind(Enum):
    Start = "start"
    Stop = "stop"
    Status = "status"
    Exit = "exit"
    Change = "change"

def check_cmd(text: str) -> CommandKind:
    try:
        return CommandKind(text)
    except:
        return None