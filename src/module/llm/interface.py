from abc import abstractmethod
from typing import Tuple

from .caller import Caller 
from .kind import CallerKind, SearcherKind
from ..interface import ModuleInterface


LLM = "llm"

class BotInterface(ModuleInterface):
    system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def __init__(self, name: str):
        super().__init__(LLM, name)

    def _load_config(self):
        pass

    def _load_sub_modules(self):
        self._add_sub_modules({
            "caller": Caller(),
        })

    @abstractmethod
    def talk(self, query: str) -> str:
        return self._caller.single_call(query)
    
    
    def check(self) -> Tuple[bool, Exception]:
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """
        try:
            self._caller.load_config()

            response = self._caller.single_call("hello", with_system_prompt=False)
            return (response != None, None) 
        except Exception as e:
            return (False, e)
    
    def caller_kind(self) -> CallerKind:
        return self._caller.kind