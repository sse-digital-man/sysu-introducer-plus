from .interface import BotInterface
from .simple import SimpleBot


# Notice 需要在此处手动选择的对话机器人
def Bot() -> BotInterface:
    return SimpleBot()