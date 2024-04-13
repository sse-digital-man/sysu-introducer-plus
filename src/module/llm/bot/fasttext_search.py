from .base import BotInterface
from ..searcher.fasttext_search import FTSearcher


class FTBot(BotInterface):
    def __init__(self):
        self.__searcher = FTSearcher(
            database_path="data/chromadb",
            model_path="cc.zh.300.bin",
            local_file_path="data/baidu.json",
        )

    def talk(self, query: str) -> str:
        return self.__searcher.search(query, 1)
