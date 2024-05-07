from enum import Enum

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