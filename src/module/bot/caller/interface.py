from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from ...interface import ModuleInterface
from ..kind import CallerKind

class CallerInterface(ModuleInterface, metaclass=ABCMeta):
    # Notice: 在抽象类中仅提供一个默认的 Prompt，不同的 LLM 可能需要分别优化
    default_system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def __init__(self, kind: str, system_prompt: str=None):
        super().__init__("caller", kind)
        self._system_prompt = system_prompt if system_prompt != None \
            else CallerInterface.default_system_prompt
    
    # 单条消息的调用（只能输入一条 query）
    @abstractmethod
    def single_call(self, query: str, with_system_prompt: bool=True) -> str:
        ...

    ''' 多条消息的调用（可以通过上下文输入）
        输入格式: {
            role: str,
            content: str
        }
    '''