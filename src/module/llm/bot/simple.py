from .base import BotInterface

class SimpleBot(BotInterface):
    def talk(self, query: str) -> str:
        return super().talk(query)