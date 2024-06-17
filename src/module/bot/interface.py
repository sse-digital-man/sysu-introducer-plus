from abc import ABCMeta, abstractmethod
from typing import Any, Dict
from enum import Enum

from module.interface import BasicModule
from .searcher.interface import SearcherInterface
from .caller.interface import CallerInterface
from .prompt import DEMONSTRATE_PROMPT, DATA_PROMPT


class BotInterface(BasicModule, metaclass=ABCMeta):
    @abstractmethod
    def talk(self, _query: str) -> str: ...

    @property
    def _caller(self) -> CallerInterface:
        return self._sub_module("caller")


class LastStrategyKind(Enum):
    REJECT = "reject"
    HYDE = "hyde"


class RagBotInterface(BotInterface, metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

        # 默认使用拒绝操作
        self._last_strategy_kind = LastStrategyKind.REJECT

    @abstractmethod
    def _preprocess(self, query: str) -> Any:
        """对消息进行预处理, 如果不需要进行预处理直接返回即可

        Args:
            _query (str): 用户消息

        Returns:
            Any: 预处理结果
        """

    def _last_strategy(self, _query: str) -> str:
        """兜底策略，当检索结果不好时执行。

        Args:
            _query (str): 用户消息

        Returns:
            str: 生成结果
        """

        if self._last_strategy_kind == LastStrategyKind.HYDE:
            raise NotImplementedError

        raise NotImplementedError

    def talk(self, query: str) -> str:
        if self._searcher is None:
            return self._caller.single_call(query)

        # 1. 对用输入进行预处理
        process_query = self._preprocess(query)

        # 2. 使用 searcher 进行向量检索
        data = self._searcher.search_with_label(process_query, 3)

        # 3. 当效果不好时使用兜底策略
        # TODO: 衡量检索效果
        if len(data) == 0:
            return self._last_strategy(query)

        # 4. prompt 合成并生成
        return self._caller.single_call(self._generate_prompt(query, data))

    def _generate_prompt(self, query, data: Dict[str, str]) -> str:
        data_str = ""
        for _id, (_query, _document) in enumerate(data.items()):
            data_str += DATA_PROMPT.format(i=_id + 1, query=_query, document=_document)

        final_query = DEMONSTRATE_PROMPT.format(query=query, data_str=data_str)

        return final_query

    @property
    def _searcher(self) -> SearcherInterface:
        return self._sub_module("searcher")
