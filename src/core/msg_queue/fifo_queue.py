from dynamic_queue import DynamicMessageQueue
from message import Message

class FIFOQueue(DynamicMessageQueue):
    def __init__(self) -> None:
        self.queue = []

    def push(self, message: Message):
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