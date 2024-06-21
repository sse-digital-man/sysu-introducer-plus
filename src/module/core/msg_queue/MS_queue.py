from message import Message, MessageKind

from .dynamic_queue import DynamicMessageQueue


class MSQueue(DynamicMessageQueue):
    """ 基于语义的多级队列 
        multi-level Semantic queues
        核心思想是:将消息按照语义分为相关和不相关两类
    """
    def __init__(self) -> None:
        # 用于存储管理员信息
        self.queue1 = []
        # 用于存储高度相关的用户信息
        self.queue2 = []
        self.queue3 = []

    def push(self, message: Message):
        # 介绍到管理员消息时，将其放在第队首
        if message.kind == MessageKind.Admin:
            self.queue1.append(message)
        else:
            # TODO:不清楚怎么这个引入searcher
            score = self._searcher.similarity(message.content)
            # 0~ 0.4 与主题相关的信息
            if score < 0.4:
                self.queue2.append(message)
            # 0.4~ 1 与主题无关的信息
            else:   
                self.queue3.append(message)

    def pop(self) -> Message:
        if len(self.queue1) != 0 :
            return self.queue1.pop(0)
        if len(self.queue2) != 0 :
            return self.queue2.pop(0)
        if len(self.queue3) != 0 :
            return self.queue3.pop(0)
        raise ValueError("the queue is empty")


    def clear(self):
        self.queue1.clear()
        self.queue2.clear()
        self.queue3.clear()


    def empty(self) -> bool:
        return len(self.queue1) == 0 and len(self.queue2) == 0 and len(self.queue3) == 0

    def __len__(self) -> int:
        return len(self.queue1) + len(self.queue2) + len(self.queue3)
