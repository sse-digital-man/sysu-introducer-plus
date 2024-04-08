from utils.config import config

from ..caller_kind import CallerKind

from .base import CallerInterface
from .gpt import GPTCaller
from .virtual import VirtualCaller


map = {
    CallerKind.GPT: GPTCaller,
    CallerKind.Virtual: VirtualCaller
}        


def Caller() -> CallerInterface:
    kind_text = config.get_use_module('llm', 'kind');
    try:
        kind = CallerKind(kind_text)
    except:
        raise KeyError("unknown kind of bot: {}".format(kind_text))
    
    return map[kind]()