from abc import ABCMeta, abstractmethod
from module.interface import BasicModule

from ..prompt import SYSTEM_PROMPT


class CallerInterface(BasicModule, metaclass=ABCMeta):
    def __init__(self, system_prompt: str = None):
        super().__init__()
        self._system_prompt = (
            system_prompt
            if system_prompt is not None
            else SYSTEM_PROMPT
        )

    def check(self):
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """
        self.single_call("hello", with_system_prompt=False)

    # 单条消息的调用（只能输入一条 query）
    @abstractmethod
    def single_call(self, query: str, with_system_prompt: bool = True) -> str: ...
