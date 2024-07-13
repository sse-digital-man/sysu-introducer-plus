from message import Message, MessageKind

from .interface import QueueInterface


class FIFOQueue(QueueInterface):
    def __init__(self):
        super().__init__()

        self.queue = []

    def load_config(self):
        pass

    def push(self, message: Message):
        # 介绍到管理员消息时，将其放在第队首
        if message.kind == MessageKind.Admin:
            self.queue.insert(0, message)
        else:
            self.queue.append(message)

    def pop(self) -> Message:
        if len(self.queue) == 0:
            raise ValueError("the queue is empty")

        return self.queue.pop(0)

    def clear(self):
        self.queue.clear()

    def empty(self) -> bool:
        return len(self.queue) == 0

    def __len__(self) -> int:
        return len(self.queue)
