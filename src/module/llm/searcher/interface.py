from abc import ABCMeta, abstractmethod
from typing import List, Dict

from ..interface import ModuleInterface

class SearcherInterface(ModuleInterface, metaclass=ABCMeta):
    Kind = "searcher"
    def __init__(self, name: str):
        super().__init__(self.Kind, name)

    @abstractmethod
    def search(self, query: str, size: int) -> List[str]:
        """返回与 query 相似的文本列表

        Args:
            query (str): 查找文本
            size (int): 查找数量

        Returns:
            List[str]: 文本列表 [text1, text2, text3, ...]
        """

    @abstractmethod
    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        """返回与 query 相似的文本列表，以及对应的标签信息(query/id)

        Args:
            query (str): 查找文本
            size (int): 查找数量

        Returns:
            Dict[str, str]: 文本字典 { query1: text1, query2: text2, ...}
        """
        ...