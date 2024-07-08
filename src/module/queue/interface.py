from abc import ABCMeta, abstractmethod

from message import Message
from ..interface import BasicModule
from module.bot.searcher.interface import SearcherInterface



class QueueInterface(BasicModule, metaclass=ABCMeta):
    @abstractmethod
    def push(self, message: Message): ...

    @abstractmethod
    def pop(self) -> Message: ...

    @abstractmethod
    def clear(self): ...

    @abstractmethod
    def empty(self) -> bool: ...

    @abstractmethod
    def __len__(self) -> int: ...
    
    @property
    def _searcher(self) -> SearcherInterface:
        return self._sub_module("searcher")