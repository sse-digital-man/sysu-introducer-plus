from message import Message, MessageKind
import threading
import math
from .interface import QueueInterface
from datetime import datetime


class TamQueue(QueueInterface):
    def __init__(self) -> None:
        super().__init__()
        self.queue1 = []
        self.queue2 = []
        self.last_time = datetime.now().timestamp()
        self.lock = threading.Lock()
        
    def load_config(self):
        pass

    def calculate_total_priority(self, current_time, last_time, sim):
        # 相似度计算公式为 - sim * (e^{-(t-t0)/30})
        time_factor = 1 / (math.exp(-(current_time - last_time)/30))
        return -sim * time_factor

    # push的时候会引起重排序
    def push(self, message: Message):
        with self.lock:
            # 介绍到管理员消息时，将其放在第一队的队首
            if message.kind == MessageKind.Admin:
                self.queue1.insert(0, message)
            else:
                message.sim = self._searcher.similarity(message.content)
                # 只有语义相关的信息(小于 0.35)才被放入
                if message.sim < 0.35:
                    self.queue2.append(message)
                    # 60s重排序一次
                    current_time = datetime.now().timestamp()
                    if (current_time - self.last_time > 60):
                        self.queue2.sort(key=lambda x: self.calculate_total_priority(x.timestamp, current_time, x.sim))
                        self.last_time = current_time


    # pop的时候不会影响
    def pop(self) -> Message:
        with self.lock:
            if len(self.queue1) != 0 :
                return self.queue1.pop(0)
            if len(self.queue2) != 0 :
                return self.queue2.pop(0)
            raise ValueError("the queue is empty")


    def clear(self):
        with self.lock:
            self.queue1.clear()
            self.queue2.clear()

    def empty(self) -> bool:
        with self.lock:
            return len(self.queue1) == 0 and len(self.queue2) == 0

    def __len__(self) -> int:
        with self.lock:
            return len(self.queue1) + len(self.queue2)