from abc import ABCMeta, abstractmethod

from message import Message

class DynamicMessageQueue(metaclass=ABCMeta):
    @abstractmethod
    def push(self, message: Message):
        ...

    @abstractmethod
    def pop(self) -> Message:
        ...

    @abstractmethod
    def clear(self):
        ...

    @abstractmethod
    def empty(self) -> bool:
        ...

    @abstractmethod
    def __len__(self) -> int:
        ...