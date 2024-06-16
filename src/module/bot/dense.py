from typing import Any
from .interface import RagBotInterface


class DenseBot(RagBotInterface):
    def load_config(self):
        pass

    # 稠密检索的 Embedding 操作在 Searcher 中实现
    def _preprocess(self, query: str) -> Any:
        return query
