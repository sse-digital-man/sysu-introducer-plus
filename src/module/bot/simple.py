from . import BotInterface

class SimpleBot(BotInterface):
    def __init__(self):
        super().__init__("simple")

    def talk(self, query: str) -> str:
        return super().talk(query)