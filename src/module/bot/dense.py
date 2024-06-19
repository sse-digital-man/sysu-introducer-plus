from typing import Any
from .interface import RagBotInterface

from .prompt import HYDE_PROMPT

class DenseBot(RagBotInterface):
    def load_config(self):
        pass

    # 稠密检索的 Embedding 操作在 Searcher 中实现
    def _preprocess(self, query: str) -> Any:
        return query

    def _last_strategy(self, _query: str) -> str:
        # 如果Searcher为空，直接返回空字典
        if self._searcher is None or self._searcher.kind != 'vector' or self._caller.kind != 'gpt':
            return self.talk(_query)
    
        # 1. 生成 hyde 假设性回答
        query = HYDE_PROMPT.format(query=_query)
        query += self._caller.single_call(query, False)

        # 2.使用 hyde 检索得到 top3 相似结果
        data = self._searcher.search_with_label(query, 3)

        # 3. prompt 合成并生成
        return self._caller.single_call(self._generate_prompt(query, data))