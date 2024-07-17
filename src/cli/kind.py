COMMANDS = {
    "start": {"usage": "[name]"},
    "stop": {"usage": "[name]"},
    "status": {"usage": "[field1] [field2] [...]"},
    "exit": {"usage": ""},
    "change": {"usage": "name kind"},
    "send": {"usage": '"content"'},
    "reload": {"usage": ""},
    "docker": {"usage": "[start|stop] name kind"},
}


def check_cmd(cmd: str) -> bool:
    return COMMANDS.get(cmd) is not None


class CommandHandleError(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


class UnknownCommandError(CommandHandleError):
    def __init__(self, *args):
        if len(args) == 0:
            args = ["unknown command"]

        super().__init__(*args)


class CommandUsageError(CommandHandleError):
    def __init__(self, cmd: str):
        usage = f"usage - {cmd} {COMMANDS[cmd]['usage']}"
        super().__init__(usage)
