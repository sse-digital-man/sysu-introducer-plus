from typing import Any
from .interface import RagBotInterface
from .prompt import KEYWORD_EXTRACT_PROMPT


class SparseBot(RagBotInterface):
    def load_config(self):
        pass

    def _preprocess(self, query: str) -> Any:
        # 1. 预处理问题,提取关键词
        p_query = self._caller.single_call(KEYWORD_EXTRACT_PROMPT % query, False)

        return p_query
