from typing import Dict, Callable
from . import ModuleLog

from .database import DATABASE

LogRecorderCallback = Callable[[ModuleLog], None]


class Logger:

    def __init__(self):
        self.__listeners: Dict[str, LogRecorderCallback] = {}

    def log(self, log: ModuleLog):
        DATABASE.append(log)

        for listener in self.__listeners.values():
            listener(log)

    def add_listener(self, name: str, callback: LogRecorderCallback):
        self.__listeners[name] = callback
