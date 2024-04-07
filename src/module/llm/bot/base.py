from abc import ABCMeta, abstractmethod
from typing import List, Tuple
import numpy as np
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
)

from ..embedding import data_collection

from ..bot_kind import BotKind


class BasicBot(metaclass=ABCMeta):
    system_prompt = "你现在是一名主播，请回答观众问题，请将回答控制在10字以内。"

    def __init__(self, kind: BotKind):
        self.__kind = kind
        pass

    # 用于重新加载配置信息
    @abstractmethod
    def _load_config(self): ...

    # 单条消息的调用（只能输入一条 query）
    @abstractmethod
    def _single_call(self, query: str) -> str: ...

    """ 多条消息的调用（可以通过上下文输入）
        输入格式: {
            role: str,
            content: str
        }
    """
    # @abstractmethod
    # def _multi_call(self, query: List[dict]) -> str:
    #     ...

    def talk(self, query: str) -> str:
        new_question_embedding = data_collection.model[query]

        closest_text = None
        closest_distance = float("inf")
        for text in data_collection.r.hkeys("knowledge_base_embeddings"):
            text_embedding = np.frombuffer(
                data_collection.r.hget("knowledge_base_embeddings", text),
                dtype=np.float32,
            )
            distance = np.linalg.norm(new_question_embedding - text_embedding)
            if distance < closest_distance:
                closest_distance = distance
                closest_text = text

        query = "对于问题“{}”，我的回答是：{}".format(
            query, closest_text.decode("utf-8")
        )
        print("query:", query)
        return self._single_call(query)

    def check(self) -> Tuple[bool, Exception]:
        """如果调用后不会报错且能够正常返回，则检验正常。
        在调用该函数时，会重新加载配置文件中的配置信息。
        因此该函数只运行一次即可。

        Returns:
            bool: 是否正常
        """

        try:
            self._load_config()

            response = self._single_call("hello")
            return (response != None, None)
        except Exception as e:
            return (False, e)

    @property
    def kind(self) -> BotKind:
        return self.__kind
