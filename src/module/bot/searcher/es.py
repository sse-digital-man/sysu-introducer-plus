from typing import Dict, List, Any
import json
from elasticsearch import Elasticsearch

from .interface import SearcherInterface
from ..prompt import KEYWORD_EXTRACT_PROMPT
from ..caller.interface import CallerInterface


class EsSearcher(SearcherInterface):
    def __init__(self):
        super().__init__()
        self._es = Elasticsearch(["http://localhost:9200"])
        self._es_index = "school_library"

    def _process(self, query: str) -> Any:
        p_query = self._caller.single_call(KEYWORD_EXTRACT_PROMPT % query, False)

        return p_query

    def handle_starting(self):
        # Notice: 不能够在 __init__() 中编写除了定义之外的操作
        self.build_index()

    def search(self, query: str, size: int) -> List[str]:
        """使用elasticsearch搜索返回与 query 相似的文本列表
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            List[str]: 文本列表 [text1, text2, text3, ...]
        """

        query = self._process(query)

        # dsl = {"query": {"match": {"query": query}}, "size": size}
        dsl = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"query": query}},
                        {"match": {"metadata": query}},
                    ],
                    "minimum_should_match": 1,
                }
            },
            "sort": [{"_score": {"order": "desc"}}],
        }
        search_res = self._es.search(index=self._es_index, body=dsl)
        res, count = [], 0
        # 遍历得到前size个相似问题
        for doc in search_res["hits"]["hits"]:
            if count >= size:
                break
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            res.append(_query + ":" + _document)
            count = count + 1
        return res

    def search_with_label(self, query: str, size: int) -> Dict[str, str]:
        """返回与 query 相似的文本列表，以及对应的标签信息(query/id)
        Args:
            query (str): 查找文本
            size (int): 查找数量
        Returns:
            Dict[str, str]: 文本字典 { query1: text1, query2: text2, ...}
        """

        query = self._process(query)

        dsl = {"query": {"match": {"query": query}}, "size": size}
        search_res = self._es.search(index=self._es_index, body=dsl)
        res = {}
        # 遍历得到前size个相似问题
        for doc in search_res["hits"]["hits"]:
            _query = doc["_source"]["query"]
            _document = doc["_source"]["document"]
            res[_query] = _document
        return res

    def build_index(self) -> bool:
        """基于数据库建立es索引
        Returns:
            bool: 是否之前就存在es索引,没有索引就建立
        """

        with open("data/database.json", "r", encoding="utf-8") as f:
            _dict = json.load(f)
        # 存在索引,且索引的数据项的size与当前数据一致时,不需要重新加载
        if self._es.indices.exists(index=self._es_index):
            result = self._es.count(index=self._es_index)
            if result["count"] == len(_dict):
                return True
            self._es.indices.delete(index=self._es_index)

        # 需要重新建立索引
        self._es.indices.create(index=self._es_index)
        for _, dict in _dict.items():
            self._es.index(index=self._es_index, body=dict)
        return False

    def load_config(self): ...

    @property
    def _caller(self) -> CallerInterface:
        return self._sub_module("caller")
