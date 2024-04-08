import time
import random as ra

from .base import BasicBot
from ..bot_kind import BotKind

from utils.config import config

RANDOM_ANSWERS = [
    "欢迎欢迎",
    "见到你很高兴",
    "谢谢夸奖",
    "你说得对"
]


class VirtualBot(BasicBot):

    def __init__(self):
        super().__init__(BotKind.Virtual)

        # 调研延迟 (单位为 ms)
        self.__delay: int
        # 生成回答策略：
        # 1. true: 从随机答案库中输出一个回答
        # 2. false: 输出我回答了 XXX
        self.__is_random: bool

    def _load_config(self):
        info = config.get_system_module("llm", self.kind.value)

        self.__delay = info['delay'] / 1000
        self.__is_random = info['isRandom']

        if self.__delay < 0:
            raise ValueError("delay must be not negative")

    def _single_call(self, query: str, use_system_prompt: bool) -> str:
        time.sleep(self.__delay)

        if self.__is_random:
            return ra.sample(RANDOM_ANSWERS, 1)[0]
        else:
            return f"我回答了 {query}"

