from . import BotInterface
from ..searcher.elastic_search import ESSearcher

class ESBot(BotInterface):
    def __init__(self):
        self.__searcher = ESSearcher()

    def talk(self, query: str) -> str:
        ...