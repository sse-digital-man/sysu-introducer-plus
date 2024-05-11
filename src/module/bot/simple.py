from . import BotInterface

class SimpleBot(BotInterface):
    def __init__(self):
        super().__init__()

    def talk(self, query: str) -> str:
        return super().talk(query)