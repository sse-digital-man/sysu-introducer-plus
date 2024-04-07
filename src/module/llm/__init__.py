from ...utils.config import config

from .bot.gpt import GPTBot
from .bot.virtual import VirtualBot
from .bot_kind import BotKind


map = {BotKind.GPT: GPTBot, BotKind.Virtual: VirtualBot}


def Bot():
    kind_text = config.get_use_module("llm", "kind")
    try:
        kind = BotKind(kind_text)
    except:
        raise KeyError("unknown kind of bot: {}".format(kind_text))

    return map[kind]()
